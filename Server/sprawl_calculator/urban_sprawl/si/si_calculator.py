import ctypes
import math

import numpy
from osgeo import gdal

from ..common import constants
from urban_sprawl.common.common import Common


class SiCalculator:
    def __init__(
        self, raster: gdal.Dataset, clipped_raster_path: numpy.ndarray, radius: int
    ):
        self._matrix = Common.get_matrix(raster)
        self._clipped_matrix = clipped_raster_path

        self._radius = radius
        self._no_data_value = constants.NO_DATA_VALUE
        self._build_up_value = constants.BUILD_UP_VALUE

        self._pixel_size = Common.get_pixel_size(raster)
        self._wcc = self._calculate_wcc(self._pixel_size)

    @staticmethod
    def _calculate_wcc(pixel_size: float) -> float:
        return math.sqrt(0.97428 * pixel_size + 1.046) - 0.996249

    def calculate(
        self, si_lib: ctypes.CDLL, x_index: int, y_index: int
    ) -> numpy.ndarray:
        shape = Common.get_shape(self._clipped_matrix)
        matrix_shape = Common.get_shape(self._matrix)

        result_matrix = numpy.full(
            shape=(shape.rows, shape.columns),
            fill_value=self._no_data_value,
            dtype=float,
        )

        ND_POINTER_2 = numpy.ctypeslib.ndpointer(dtype=numpy.uint8, ndim=2, flags="C")

        si_lib.calc.argtypes = [
            ND_POINTER_2,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_int32,
            ctypes.c_double,
            ctypes.c_int32,
            ctypes.c_int32,
        ]
        si_lib.calc.restype = ctypes.c_double
        offset = round(self._radius / self._pixel_size)

        for x in range(0, shape.rows):
            for y in range(0, shape.columns):
                if self._clipped_matrix[x, y] == self._build_up_value:
                    x_with_offset = x + x_index
                    y_with_offset = y + y_index
                    result = si_lib.calc(
                        self._matrix,
                        matrix_shape.rows,
                        matrix_shape.columns,
                        x_with_offset,
                        y_with_offset,
                        int(self._pixel_size),
                        self._wcc,
                        offset,
                        self._build_up_value,
                    )
                    result_matrix[x, y] = result

        return result_matrix
