from src.common import safe_int
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.pair_value_operations.pair_values_operation import PairValuesOperation


class XorOperation(PairValuesOperation):
    def __init__(self) -> None:
        super().__init__(name="^")

    def calculate(self, first: str, second: str) -> str:
        int_first = safe_int(first)
        int_second = safe_int(second)
        if not (isinstance(int_first, int) and isinstance(int_second, int)):
            raise EvaluationError("XorSupportIntsOnly")
        try:
            return str(int_first ^ int_second)
        except Exception as e:
            raise EvaluationError(f"XorFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Xor operation
        @symbol: ^
        @first_parameter: Integer
        @second_parameter: Integer
        @returns: first number xor the second
        """
