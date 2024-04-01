from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.pair_value_operations.pair_values_operation import PairValuesOperation


class MultiplyingOperation(PairValuesOperation):
    def __init__(self) -> None:
        super().__init__(name="*")

    def calculate(self, first: str, second: str) -> str:
        parsed_first = safe_float(first)
        parsed_second = safe_float(second)
        if not (isinstance(parsed_first, float) and isinstance(parsed_second, float)):
            raise EvaluationError("MultiplyingSupportNumbersOnly")
        try:
            return str(parsed_second * parsed_first)
        except Exception as e:
            raise EvaluationError(f"FailedMultiplying {first}*{second}")

    @property
    def documentation(self) -> str:
        return """
        Multiplying operation
        @symbol: *
        @first_parameter: Number
        @second_parameter: Number
        @returns: first number * second number
        """
