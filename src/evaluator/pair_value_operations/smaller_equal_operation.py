from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.pair_value_operations.pair_values_operation import PairValuesOperation


class SmallerEqualOperation(PairValuesOperation):
    def __init__(self) -> None:
        super().__init__(name="<=")

    def calculate(self, first: str, second: str) -> str:
        try:
            float_first = safe_float(first)
            float_second = safe_float(second)
            if isinstance(float_first, float) and isinstance(float_second, float):
                if float_first <= float_second:
                    return "1"
            elif first <= second:
                return "1"
            return "0"
        except Exception as e:
            raise EvaluationError(f"SmallerEqualFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Smaller Equal operation
        @symbol: <=
        @first_parameter: Any
        @second_parameter: Any
        @returns: 1: first smaller or equal to the second
                  0: otherwise 
        try to compare them as numbers
        """
