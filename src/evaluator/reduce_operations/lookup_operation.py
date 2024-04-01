from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation


class LookupOperation(ReduceOperation):
    def __init__(self) -> None:
        super().__init__(name="LOOKUP")

    def calculate(self, table: list[list[str]]) -> str:
        if len(table) % 2 == 0 and len(table) > 3:
            raise EvaluationError("Lookup invalid input")
        try:
            mid = len(table) // 2
            search = table[:mid]
            data = table[mid]
            target = [col[0] for col in table[mid + 1:]]

            for i in range(len(search[0])):
                if target == [search[j][i] for j in range(mid)]:
                    return data[i]
        except Exception as e:
            raise EvaluationError("LookUpFailed")
        return "NoResults"

    @property
    def documentation(self) -> str:
        return """
        LookUp Function
        for more description, see python math.log
        @symbol: LN 
        
        @parameters: (INPUT COLS) (RESULT COL) (TARGET COLS)
        INPUT and target COLS must have the same amount of columns.
        target column should be only one row, 
        any more values there will be ignored and the first row of the target cols will be used
        
        @returns: RESULT where target matches input

        A B C D E
        1 2 a 
        2 3 b 1 2 
        3 4 c
                       input result target
        @Example: LookUp(A:B, C:C, D2:E2) -> a  
        
        @Warning: space sensitive, so be aware
        
        """
