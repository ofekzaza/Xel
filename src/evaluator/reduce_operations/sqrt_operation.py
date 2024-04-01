import math

from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class SqrtOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="SQRT")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) != 1 or len(table[0]) != 1:
            raise EvaluationError("SqrtInvalidAmountOfArgs")

        value = safe_float(table[0][0])
        if not isinstance(value, float):
            raise EvaluationError("SqrtMustBeNumber")

        try:
            return str(math.sqrt(value))
        except Exception as e:
            raise EvaluationError("SqrtFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Sqrt Function
        @symbol: SQRT
        @parameters: A Number - value to sqrt
        @returns: square root of input
        """
