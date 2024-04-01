from typing import Union, List, Dict, Any

from .exceptions.evaluation_error import EvaluationError
from .pair_value_operations.pair_values_operation import PairValuesOperation
from .reduce_operations.reduce_operation import ReduceOperation


class EquationEvaluator:
    """
    parsed Equation calculator
    """
    def __init__(
            self,
            ordered_pair_operations: List[PairValuesOperation],
            reduce_operations: Dict[str, ReduceOperation]
    ) -> None:
        self.ordered_pair_operations = ordered_pair_operations
        self.reduce_operations = reduce_operations

    def evaluate(self, tokens: Union[str, list[Any]]) -> Union[str, list[Any]]:
        """
        Evaluates the parsed expression using a stack-based approach.
        """
        if not isinstance(tokens, list):
            return str(tokens)

        if len(tokens) == 1 and not isinstance(tokens[0], list):
            return self.evaluate(tokens[0])

        stack = self._evaluator_reduce_operations(tokens)
        stack = self._evaluate_pair_values_operations(stack)

        if len(stack) != 1:
            raise EvaluationError("InvalidEquation")

        return str(stack.pop())

    def _evaluator_reduce_operations(self, tokens: list[Any]) -> list[Any]:
        """
        :param tokens: parsed equation
        :return: equation where all functions are replaced with their values
        """
        stack = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if isinstance(token, list):  # handle parenthesis
                stack.append(self.evaluate(token))
            elif token in self.reduce_operations:
                evaluated_token = [[str(self.evaluate(item)) for item in row] for row in tokens[i + 1]]
                reduced_token = self.reduce_operations[token].calculate(evaluated_token)
                stack.append(reduced_token)
                i += 1
            else:
                stack.append(token)
            i += 1
        return stack

    def _evaluate_pair_values_operations(self, stack: list[Any]) -> list[Any]:
        """

        :param stack: equation
        :return: equation where all operands have been replaces with matching calculation
        """
        calculated_stack: list[Any] = []

        for operation in self.ordered_pair_operations:
            i = 0
            while i < len(stack):
                token = stack[i]
                if token == operation.name:
                    first = str(self.evaluate(calculated_stack[-1]))
                    second = str(self.evaluate(stack[i + 1]))
                    result = operation.calculate(first, second)
                    calculated_stack[-1] = result
                    i += 2
                else:
                    calculated_stack.append(token)
                    i += 1

            stack = calculated_stack
            calculated_stack = []
            if len(stack) == 1:
                return stack

        return stack
