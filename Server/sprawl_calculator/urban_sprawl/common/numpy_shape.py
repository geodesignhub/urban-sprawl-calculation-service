from typing import Tuple


class NumpyShape:
    def __init__(self, rows: int, columns: int):
        self._rows = rows
        self._columns = columns

    def __str__(self) -> str:
        return f"NumpyShape(rows={self._rows}, columns={self._columns})"

    @staticmethod
    def parse(value: Tuple[int, int]) -> "NumpyShape":
        (rows, columns) = value
        return NumpyShape(rows, columns)

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns
