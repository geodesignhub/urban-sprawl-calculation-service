from typing import Callable, Any
import re
from osgeo import gdal
import numpy

from qgis.core import QgsFeature

from ..common import constants
from ..common.gdal_geo_transform import GdalGeoTransform
from ..common.numpy_shape import NumpyShape


class Common:
    @staticmethod
    def get_geo_transform(raster: gdal.Dataset) -> GdalGeoTransform:
        return GdalGeoTransform.parse(raster.GetGeoTransform())

    @staticmethod
    def get_shape(matrix: numpy.ndarray) -> NumpyShape:
        return NumpyShape.parse(matrix.shape)

    @staticmethod
    def get_pixel_size(raster: gdal.Dataset) -> float:
        geo_transform = Common.get_geo_transform(raster)

        if geo_transform.pixel_size_x == geo_transform.pixel_size_y:
            return geo_transform.pixel_size_x
        else:
            raise ValueError("Pixels are not square")

    @staticmethod
    def get_matrix(raster: gdal.Dataset) -> numpy.ndarray:
        return numpy.array(raster.GetRasterBand(1).ReadAsArray(), dtype=numpy.uint8)

    @staticmethod
    def get_area(
        raster: numpy.ndarray,
        pixel_size: float,
        selection_function: Callable[[float], bool],
    ) -> float:

        shape = Common.get_shape(raster)

        count = 0
        for x in range(0, shape.rows):
            for y in range(0, shape.columns):
                if selection_function(raster[x, y]):
                    count += 1

        return (pixel_size ** 2) * count

    @staticmethod
    def get_clipped_raster_name(parameters: Any, feature: QgsFeature) -> str:
        feature_name = ""
        if (
            parameters[constants.NAME_FIELD]
            and feature[parameters[constants.NAME_FIELD]]
        ):
            feature_name = re.sub(
                "[/,\\\\ .]", "_", str(feature[parameters[constants.NAME_FIELD]])
            )
        return feature_name
