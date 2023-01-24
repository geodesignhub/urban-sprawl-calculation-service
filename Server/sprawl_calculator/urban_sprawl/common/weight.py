import math


def get_weighted_lup(lup_value: float) -> float:
    value1 = math.exp(4.159 - 613.125 / lup_value)
    return value1 / (1 + value1)


def get_weighted_dis(dis_value: float) -> float:
    value2 = math.exp(0.294432 * dis_value - 12.955)
    return value2 / (1 + value2)


def get_weighted_ud(ud_value: float) -> float:
    value = math.exp(4.159 - 0.000613125 * ud_value)
    return value / (1 + value)
