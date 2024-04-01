from src.common import safe_float
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class CountIfOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="COUNTIF")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) < 2:
            return "0"
        try:
            target = safe_float(table[-1][0])
            counter = 0
            for row in table[:-1]:
                for item in row:
                    if safe_float(item) == target:
                        counter += 1
            return str(counter)
        except Exception as e:
            raise EvaluationError("COUNTIFFailed") from e

    @property
    def documentation(self) -> str:
        return """
        CountIf Function
        @symbol: COUNTIF 
        @parameters: (Table, condition) 
                condition is a string, it is always the first element of the last column
        @returns: every element which is equal to the condition.
        @Example: COUNTIF(1,2,3,4, 2, 2) -> "2"
        """
