from src.common import safe_int
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class TruncateOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="TRUNC")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) != 2 and len(table[0]) != 1 and len(table[1]) != 1:
            raise EvaluationError("TRUNCInvalidInput")

        length = safe_int(table[1][0])
        if not isinstance(length, int):
            raise EvaluationError("TRUNCLengthIsNotInt")

        if length < 1:
            raise EvaluationError("TRUNCLenMustBePositive")

        try:
            return table[0][0][:length]
        except Exception as e:
            raise EvaluationError("Failed truncate operation") from e

    @property
    def documentation(self) -> str:
        return """
        Truncate Function
        @symbol: TRUNC
        @parameters: (String, Integer)
                value can be any string
                length must be an integer
        @returns: value as length
            version without all chars after value[length]
        """
