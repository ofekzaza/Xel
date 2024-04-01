from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.pair_value_operations.pair_values_operation import PairValuesOperation


class AndOperation(PairValuesOperation):
    def __init__(self) -> None:
        super().__init__(name="&")

    def calculate(self, first: str, second: str) -> str:
        try:
            if safe_float(first) == 1.0 and safe_float(second) == 1:
                return "1"
            return "0"
        except Exception as e:
            raise EvaluationError(f"AndFailed") from e

    @property
    def documentation(self) -> str:
        return """
        And operation
        @symbol: &
        @first_parameter: Any
        @second_parameter: Any 
        @returns: 1 if both parameters are 1 otherwise returns a 0
        """
