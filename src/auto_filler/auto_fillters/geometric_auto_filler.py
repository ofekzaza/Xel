from typing import List

from src.auto_filler.cell_data import CellData
from src.auto_filler.auto_fillters import BaseAutoFiller
from src.auto_filler.direction import Direction
from src.models.cell import Cell


class GeometricAutoFiller(BaseAutoFiller):
    """
    create new cell data by calculating a power between the cells
    and the multiplying this power on the last cell/ prediction
    Example:
        1, 2, 4, -> 8, 16, 32...
        -3, 6, -12 -> 24, -48, 96...
    """
    def all_have_same_diff(self, line: List[float]) -> bool:
        if not line[0]:
            return False
        start_diff = line[1] / line[0]
        for i in range(1, len(line) - 1):
            if line[0] == 0 or start_diff != line[i + 1] / line[i]:
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
        diff = floated[1] / floated[0]
        filled = []
        new = floated[-1]
        for i in range(length):
            new *= diff
            filled.append(CellData(data=str(new), evaluation=str(new)))
        return filled
