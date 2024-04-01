from collections import Iterable
import statistics

from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class AverageOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="AVG")

    def calculate(self, table: Iterable[Iterable[str]]) -> str:
        cells = []
        for row in table:
            for cell in row:
                floated = safe_float(cell)
                if isinstance(floated, float):
                    cells.append(floated)
        try:
            return str(statistics.mean(cells))
        except Exception as e:
            raise EvaluationError("AVGFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Average Function
        @symbol: ABS 
        @parameters: Table of Numbers
                     Ignore values which are not numbers
        @returns: average of the entire table
            sum(cells) / length(cells)
        """
