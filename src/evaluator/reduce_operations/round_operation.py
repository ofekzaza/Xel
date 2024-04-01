from src.common import safe_float, safe_int
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class RoundOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="ROUND")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) not in [1, 2]:
            raise EvaluationError("RoundInvalidAmountOfInputs")

        value = safe_float(table[0][0])
        if not isinstance(value, float):
            raise EvaluationError("RoundParameterIsNotNumber")

        digits = 0
        if len(table) > 1:
            possible_digits = safe_int(table[1][0])
            if not isinstance(digits, int):
                raise EvaluationError("RoundDigitsIsNotInteger")
            digits = int(possible_digits)

        try:
            rounded = round(value, digits) if digits else round(value)
            return str(rounded)
        except Exception as e:
            raise EvaluationError("RoundFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Round Function
        @symbol: ROUND
        @parameters: A Number - value to round
             Optional[Integer] amount of digits that will stay,
                                default is zero
        @returns: value with the amount of specified digits,
                if specified 0 digits, will return an int 
        """
