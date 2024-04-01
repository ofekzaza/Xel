from typing import List

from src.auto_filler.cell_data import CellData
from src.auto_filler.auto_fillters import BaseAutoFiller
from src.auto_filler.direction import Direction
from src.models.cell import Cell


class CopyAutoFiller(BaseAutoFiller):
    """
    Create cell data by copy paste the last cell in the line
    """
    def can_auto_fill(self, line: List[Cell]) -> bool:
        return len(line) > 0

    def auto_fill(self, line: List[Cell], length: int, direction: Direction) -> List[CellData]:
        first_data = line[0].data
        for cell in line[1:]:
            if cell.data != first_data:
                return [CellData(data=line[-1].evaluation, evaluation=line[-1].evaluation) for i in range(length)]

        return [CellData(data=line[-1].data, evaluation=line[-1].evaluation) for i in range(length)]
