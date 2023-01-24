class WspcCalculator:
    def __init__(
        self, area: float, number_of_inhabitans_and_employees: int, wup: float
    ):
        self._area = area
        self._nr_inhabitans_and_employees = number_of_inhabitans_and_employees
        self._wup = wup

    def calculate(self) -> float:
        return (self._area / self._nr_inhabitans_and_employees) * self._wup
