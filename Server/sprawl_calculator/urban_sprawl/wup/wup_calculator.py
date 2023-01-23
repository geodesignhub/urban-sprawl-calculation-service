from ..common.weight import get_weighted_lup, get_weighted_dis


class WupCalculator:
    def __init__(self, up_value: float, dis_value: float, lup_value: float):
        self._up_value = up_value
        self._dis_value = dis_value
        self._lup_value = lup_value

    def calculate(self) -> float:

        if self._up_value < 0:
            return 0

        return (
            self._up_value
            * get_weighted_lup(self._lup_value)
            * (0.5 + get_weighted_dis(self._dis_value))
        )
