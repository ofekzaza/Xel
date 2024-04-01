from typing import List

from src.auto_filler.cell_data import CellData
from src.auto_filler.auto_fillters import ArithmeticAutoFiller, \
    CopyAutoFiller, \
    BaseAutoFiller, \
    GeometricAutoFiller
from src.auto_filler.direction import Direction
from src.common import pivot_table
from src.models.cell import Cell


class AutoFillerFactory:
    """
    factory design pattern for auto fillers
    this is a factory by priority,
    meaning the first algorithm which matches will be used.
    """

    def __init__(self) -> None:
        self.auto_fillers: List[BaseAutoFiller] = [
            ArithmeticAutoFiller(),
            GeometricAutoFiller(),
            CopyAutoFiller(),
        ]

    def auto_fill(self, table: List[List[Cell]], length: int, direction: Direction) -> List[List[CellData]]:
        """
        create data predictions based on table of cells.
        :param table: table of cells, normally selected cells from the ui
        :param length: length of each line of prediction
        :param direction: UP/Down/Right/Left
        :return: table of predictions
        """
        if not table or length < 1:
            return []

        return self._generate_data_predictions(direction, length, table)

    def _generate_data_predictions(
            self,
            direction: Direction,
            length: int,
            table: List[List[Cell]]
    ) -> List[List[CellData]]:
        predictions = []
        lines = table
        if direction in [Direction.DOWN, Direction.UP]:
            lines = pivot_table(table)
        for line in lines:
            if direction in [Direction.UP, Direction.LEFT]:
                line.reverse()
            prediction = self._auto_fill_line(line, length, direction)
            if direction in [Direction.UP, Direction.LEFT]:
                prediction.reverse()
            predictions.append(prediction)
        if direction in [Direction.DOWN, Direction.UP]:
            predictions = pivot_table(predictions)
        return predictions

    def _auto_fill_line(self, line_in_direction: List[Cell], length: int, direction: Direction) -> List[CellData]:
        """
        detect relevant autofiller for the line and than autofill a like
        :param line_in_direction: ordered cells
        :param length: amount of cells to predict for the line
        :param direction: in which direction the line is in the table
        :return: line of predictions in the direction.
        """
        for auto_filler in self.auto_fillers:
            if auto_filler.can_auto_fill(line_in_direction):
                return auto_filler.auto_fill(line_in_direction, length, direction)

        return []
