from collections import Iterable

from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class CountOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="COUNT")

    def calculate(self, table: Iterable[Iterable[str]]) -> str:
        try:
            length = sum(1 for row in table for cell in row)
            return str(length)
        except Exception as e:
            raise EvaluationError("COUNTFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Count Function
        @symbol: COUNT 
        @parameters: Table
        @returns: amount of elements in table.
        @Example: COUNT(1,2,3,4) -> "4"
        """
