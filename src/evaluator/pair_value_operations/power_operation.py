from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.pair_value_operations.pair_values_operation import PairValuesOperation


class PowerOperation(PairValuesOperation):
    def __init__(self) -> None:
        super().__init__(name="**")

    def calculate(self, first: str, second: str) -> str:
        parsed_first = safe_float(first)
        parsed_second = safe_float(second)
        if not (isinstance(parsed_first, float) and isinstance(parsed_second, float)):
            raise EvaluationError("PowerSupportNumbersOnly")
        try:
            return str(parsed_first ** parsed_second)
        except Exception as e:
            raise EvaluationError(f"FailedPowering {first} by {second}") from e

    @property
    def documentation(self) -> str:
        return """
        Power operation (exponent by second parameter)
        @symbol: **
        @first_parameter: Number
        @second_parameter: Number
        @returns: first number powered by the second number
        """
