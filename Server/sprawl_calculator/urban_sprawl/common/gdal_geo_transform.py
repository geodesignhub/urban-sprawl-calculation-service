from typing import Tuple


class GdalGeoTransform:
    def __init__(
        self,
        position_x: float,
        pixel_size_x: float,
        rotation_x: float,
        position_y: float,
        rotation_y: float,
        pixel_size_y: float,
    ):
        self._position_x = position_x
        self._position_y = position_y

        self._pixel_size_x = abs(pixel_size_x)
        self._pixel_size_y = abs(pixel_size_y)

        self._rotation_x = rotation_x
        self._rotation_y = rotation_y

    def __str__(self) -> str:
        return (
            "GdalGeoTransform("
            f"position_x={self._position_x}, position_y={self._position_y}, "
            f"pixel_size_x={self._pixel_size_x}, pixel_size_y={self._pixel_size_y}, "
            f"rotation_x={self._rotation_x}, rotation_y={self._rotation_y}"
            ")"
        )

    @staticmethod
    def parse(
        value: Tuple[float, float, float, float, float, float]
    ) -> "GdalGeoTransform":
        (
            position_x,
            pixel_size_x,
            rotation_x,
            position_y,
            rotation_y,
            pixel_size_y,
        ) = value
        return GdalGeoTransform(
            position_x, pixel_size_x, rotation_x, position_y, rotation_y, pixel_size_y
        )

    @property
    def position_x(self) -> float:
        return self._position_x

    @property
    def position_y(self) -> float:
        return self._position_y

    @property
    def pixel_size_x(self) -> float:
        return self._pixel_size_x

    @property
    def pixel_size_y(self) -> float:
        return self._pixel_size_y

    @property
    def rotation_x(self) -> float:
        return self._rotation_x

    @property
    def rotation_y(self) -> float:
        return self._rotation_y
