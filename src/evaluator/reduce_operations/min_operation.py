from collections import Iterable

from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class MinOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="MIN")

    def calculate(self, table: Iterable[Iterable[str]]) -> str:
        try:
            cells = []
            for row in table:
                for cell_to_float in row:
                    floated = safe_float(cell_to_float)
                    if not isinstance(floated, float):
                        return str(min(cell for row in table for cell in row))
                    cells.append(floated)
            return str(min(cells))
        except Exception as e:
            raise EvaluationError("MinFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Min Function
        @symbol: MIN
        @parameters: A Table
        @returns: the smallest number, 
                  or the lowest string 
        """
