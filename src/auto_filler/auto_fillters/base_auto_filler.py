from abc import ABC, abstractmethod
from typing import List

from src.auto_filler.cell_data import CellData
from src.auto_filler.direction import Direction
from src.models.cell import Cell


class BaseAutoFiller(ABC):
    @abstractmethod
    def can_auto_fill(self, line: List[Cell]) -> bool:
        """
        :param line: ordered cells
        :return: if auto filler can predict this line of cells
        """
        pass

    @abstractmethod
    def auto_fill(self, line: List[Cell], length: int, direction: Direction) -> List[CellData]:
        """

        :param line: ordered cells
        :param length: amount of new cells to create
        :param direction: where the line is headed
        :return: length amount of new data cells
        """
        pass
