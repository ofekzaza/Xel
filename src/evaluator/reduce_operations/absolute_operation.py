from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class AbsoluteOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="ABS")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) != 1 and len(table[0]) != 1:
            raise EvaluationError("AbsInvalidInput")

        floated = safe_float(table[0][0])
        if not isinstance(floated, float):
            raise EvaluationError("AbsInputMustBeNumber")

        try:
            return str(abs(floated))
        except Exception as e:
            raise EvaluationError("ABSFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Abs Function
        @symbol: ABS 
        @parameters: (Number)
        @returns: not negative version of the number
        @Example: ABS(-7) -> 7
        @Example: ABS(3) -> 3
        """
