import numpy

from urban_sprawl.common.common import Common


class DisCalculator:
    def __init__(self, si_raster: numpy.ndarray):
        self._si_raster = si_raster

    def calculate(self) -> float:
        shape = Common.get_shape(self._si_raster)

        count = 0
        for x in range(0, shape.rows):
            for y in range(0, shape.columns):
                if self._si_raster[x, y] > 0:
                    count += 1

        if count != 0:
            return float(numpy.sum(self._si_raster) / count)
        else:
            return -1.0
