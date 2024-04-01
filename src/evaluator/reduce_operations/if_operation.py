from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class IfOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="IF")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) != 3:
            return "IfRequire3Parameters"
        try:
            if safe_float(table[0][0]) == 1.0:
                return str(table[1][0])
            return str(table[2][0])
        except Exception as e:
            raise EvaluationError("Failed average operation") from e

    @property
    def documentation(self) -> str:
        return """
        If Function
        @symbol: IF 
        @parameters: (Boolean, ifTrue, ifFalse)
        @returns: if Boolean == 1 than return ifTrue,
                    otherwise return ifFalse
        @Example: IF(1,YES,NO) -> "YES"
        @Example: IF(value,YES,NO) -> "NO"
        """
