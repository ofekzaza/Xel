from collections import Iterable
import statistics

from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class MedianOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="MED")

    def calculate(self, table: Iterable[Iterable[str]]) -> str:
        cells = []
        for row in table:
            for cell in row:
                floated = safe_float(cell)
                if isinstance(floated, float):
                    cells.append(floated)
        try:
            return str(statistics.median(cells))
        except Exception as e:
            raise EvaluationError("MedFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Median Function
        @symbol: MED
        @parameters: A Table of numbers
                     Ignore cells which are not numbers
        @returns: the middle number in the table, 
                  half are bigger than him, 
                  half are smaller than him
        """
