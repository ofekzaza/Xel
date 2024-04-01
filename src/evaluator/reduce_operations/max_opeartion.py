from collections import Iterable

from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class MaxOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="MAX")

    def calculate(self, table: Iterable[Iterable[str]]) -> str:
        try:
            cells = []
            for row in table:
                for cell_to_float in row:
                    floated = safe_float(cell_to_float)
                    if not isinstance(floated, float):
                        return str(max(cell for row in table for cell in row))
                    cells.append(floated)
            return str(max(cells))
        except Exception as e:
            raise EvaluationError("MaxFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Max Function
        @symbol: MAX
        @parameters: Table
        @returns: the biggest number, 
                  or the highest string 
        """
