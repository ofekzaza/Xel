from collections import Iterable

from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class SummaryOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="SUM")

    def calculate(self, table: Iterable[Iterable[str]]) -> str:
        cells = []
        for row in table:
            for cell in row:
                floated = safe_float(cell)
                if isinstance(floated, float):
                    cells.append(floated)
        try:
            return str(sum(cells))
        except Exception as e:
            raise EvaluationError("SumFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Summary Function
        @symbol: SUM
        @parameters: A Table of numbers
        @returns: the summary of all the numbers in the table, 
                  ignore values which are not numbers
        """
