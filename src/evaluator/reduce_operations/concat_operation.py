from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class ConcatOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="CONCAT")

    def calculate(self, table: list[list[str]]) -> str:
        try:
            contacted = ""
            for row in table:
                for cell in row:
                    contacted += str(cell)
            return contacted
        except Exception as e:
            raise EvaluationError("ConcatFailed") from e

    @property
    def documentation(self) -> str:
        return """
        Concat Function
        @symbol: CONCAT 
        @parameters: Table of string
        @returns: one string, uniting all the cells of the table
             uniting the table row by row and from left to right.
        @Example: CONCAT(1,2,3,4) -> "1234"
        """
