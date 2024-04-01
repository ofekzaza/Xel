from typing import List

from src.auto_filler.cell_data import CellData
from src.auto_filler.auto_fillters import BaseAutoFiller
from src.auto_filler.direction import Direction
from src.models.cell import Cell


class ArithmeticAutoFiller(BaseAutoFiller):
    """
    create new cell data by calculating a diff between the cells
    and the adding this diff to the last cell, repeat
    Example:
        1, 2, 3, -> 4, 5, 6...
        8, 11, 14 -> 17, 20, 23, 26...
    """
    def all_have_same_diff(self, line: List[float]) -> bool:
        start_diff = line[1] - line[0]
        if start_diff == 0:  # for that we have copy
            return False

        for i in range(1, len(line) - 1):
            if start_diff != line[i + 1] - line[i]:
                return False
        return True

    def can_auto_fill(self, line: List[Cell]) -> bool:
        if len(line) < 2:
            return False
        try:
            floated = [float(cell.evaluation) for cell in line]
        except Exception:
            return False
        return self.all_have_same_diff(floated)

    def auto_fill(self, line: List[Cell], length: int, direction: Direction) -> List[CellData]:
        floated = [float(cell.evaluation) for cell in line]
        diff = floated[1] - floated[0]
        filled = []
        new = floated[-1]
        for i in range(length):
            new += diff
            filled.append(CellData(data=str(new), evaluation=str(new)))
        return filled
