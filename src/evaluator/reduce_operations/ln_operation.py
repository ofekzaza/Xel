import math

from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class LnOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="LN")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) != 1 and len(table[0]) != 0:
            raise EvaluationError("Ln operation got invalid input")
        floated = float(table[0][0])
        if not isinstance(floated, float):
            raise EvaluationError("LnInputMustBeNumbers")
        try:
            logged = math.log(floated)
            return str(logged)
        except Exception as e:
            raise EvaluationError("LNFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Ln Function
        @Description log with base e
        for more description, see python math.log
        @symbol: LN 
        @parameters: A Number
        @returns: Ln(Parameter) 
        @Example: LN(e) -> 1
        """