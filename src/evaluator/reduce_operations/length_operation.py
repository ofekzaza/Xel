from collections import Iterable

from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class LengthOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="LEN")

    def calculate(self, table: Iterable[Iterable[str]]) -> str:
        try:
            length = sum(len(str(cell)) for row in table for cell in row)
            return str(length)
        except Exception as e:
            raise EvaluationError("LENFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Length Function
        @symbol: LEN 
        @parameters: Table
        @returns: amount of chars in the table
        @Example: IF(1,YES,NO) -> 6
        @Example: IF(value,YES,NO,-1) -> 12
        """
