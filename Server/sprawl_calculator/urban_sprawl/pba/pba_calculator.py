# from qgis._core import QgsProcessingException


class PbaCalculator:
    def __init__(self, build_up_area: float, feat_area: float):
        self._build_up_area = build_up_area
        self.whole_area = feat_area

    def calculate(self) -> float:

        # Get PBA Value
        pba_value = self._build_up_area / self.whole_area

        # if pba_value < 0:
        #     raise QgsProcessingException("PBA value needs to be between 0% and 100%")

        return min(pba_value, 1)
