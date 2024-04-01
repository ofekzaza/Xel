import math

from src.common import safe_int
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class LogOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="LOG")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) not in [1, 2]:
            raise EvaluationError("Log operation got invalid input")
        value = float(table[0][0])
        if not isinstance(value, float):
            raise EvaluationError("LogValueMustBeNumber")

        base = safe_int(table[1][0]) if len(table) > 1 else 2
        if not isinstance(base, int):
            raise EvaluationError("LogBaseIsNotInt")

        try:
            logged = math.log(value, base)
            return str(logged)
        except Exception as e:
            raise EvaluationError("LogFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Log Function
        @symbol: LOG
        @parameters: A Number - value to log
             Optional[Integer] base of log, default base is 2
        @returns: Log(value, base) 
        """