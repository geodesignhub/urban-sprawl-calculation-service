from typing import Any

# from qgis.core import (
#     QgsProcessingFeedback,
#     QgsFeature,
# )

from ..common import constants


class LupCalculator:
    def __init__(
        self, build_up_area: float, resident_employee_count: int,
    ):
        self._resident_employee_count = resident_employee_count
        self._build_up_area = build_up_area

    def calculate(self) -> float:
        if self._resident_employee_count <= 0:
            return -1.0

        return self._build_up_area / self._resident_employee_count

    # @staticmethod
    # def check_lup_input(
    #     feat: QgsFeature, feedback: QgsProcessingFeedback, parameters: Any
    # ) -> int:
    #     resident_employee_count = 0
    #     number_of_inhabitants = 0
    #     if parameters[constants.INHABITANT_FIELD]:
    #         number_of_inhabitants = feat[parameters[constants.INHABITANT_FIELD]]
    #     number_of_employees = 0
    #     if parameters[constants.EMPLOYEE_FIELD]:
    #         number_of_employees = feat[parameters[constants.EMPLOYEE_FIELD]]
    #     if not number_of_employees and not number_of_inhabitants:
    #         feedback.reportError("The Number of residents or employees are null")
    #     else:
    #         if number_of_employees and number_of_employees > 0:
    #             resident_employee_count += int(number_of_employees)
    #         if number_of_inhabitants and number_of_inhabitants > 0:
    #             resident_employee_count += int(number_of_inhabitants)
    #     return resident_employee_count

    @staticmethod
    def verify_lup_input(
        number_of_employees:int =0 , number_of_inhabitants:int=0) -> int:
        resident_employee_count = 0
    
        if number_of_employees and number_of_employees > 0:
            resident_employee_count += int(number_of_employees)
        if number_of_inhabitants and number_of_inhabitants > 0:
            resident_employee_count += int(number_of_inhabitants)
        return resident_employee_count
