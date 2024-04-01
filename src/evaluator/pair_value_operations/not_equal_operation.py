from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.pair_value_operations.pair_values_operation import PairValuesOperation


class NotEqualOperation(PairValuesOperation):
    def __init__(self) -> None:
        super().__init__(name="<>")

    def calculate(self, first: str, second: str) -> str:
        try:
            if safe_float(first) != safe_float(second):
                return "1"
            return "0"
        except Exception as e:
            raise EvaluationError(f"NotEqualFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Not Equal operation
        @symbol: <>
        @first_parameter: Any
        @second_parameter: Any
        @returns: 1: both parameters are not the same
                  0: otherwise 
        try to compare them as numbers
        """
