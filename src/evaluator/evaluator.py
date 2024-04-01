from typing import Set, Tuple, List, Dict

from src.evaluator.dependency_manager import DependencyManager
from src.evaluator.equation_evaluator import EquationEvaluator
from src.evaluator.equation_parser import EquationParser
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.evaluator.pair_value_operations.pair_values_operation import PairValuesOperation
from src.evaluator.reduce_operations.reduce_operation import ReduceOperation
from src.models.cell import Cell
from src.models.location import Location
from src.models.workbook import Workbook


class Evaluator:
    """
    Takes cell data and returns the evaluation
    """
    def __init__(
            self,
            workbook: Workbook,
            ordered_pair_operations: List[PairValuesOperation],
            reduce_operations: List[ReduceOperation]
    ) -> None:
        self.workbook = workbook
        self.ordered_pair_operations: List[PairValuesOperation] = ordered_pair_operations
        self.reduce_operations: \
            Dict[str, ReduceOperation] = {operation.name: operation for operation in reduce_operations}

        self.equation_parser = EquationParser(
            workbook,
            {operation.name for operation in ordered_pair_operations},
            set(self.reduce_operations.keys())
        )
        self.equation_evaluator = EquationEvaluator(ordered_pair_operations, self.reduce_operations)
        self.dependency_manager = DependencyManager()

    def evaluate(self, cell: Cell, new_data: str) -> str:
        """
        update cell data and evaluation by using new_data and evaluating him
        :param cell: cell of evaluation
        :param new_data: cell new data, what to evaluate
        :return: new evaluation
        """
        try:
            evaluation, cell_dependencies = self._evaluate(new_data, cell.location)

            all_dependent_on_cell = self.dependency_manager.update_dependencies(cell.location, cell_dependencies)
            original_evaluation = cell.evaluation
            cell.set_data(new_data, evaluation)
            if original_evaluation != evaluation:  # update all if the evaluation actually changed
                self._update_all_dependent_on_cell(all_dependent_on_cell)

        except EvaluationError as e:
            cell.set_data(new_data, f"InvalidEquation:{e.message}")

        return cell.evaluation

    def _update_all_dependent_on_cell(self, all_dependent_on_cell: Set[Location]) -> None:
        """
        reevaluate all cells which use evaluated cell data.
        :param all_dependent_on_cell: all the cells which use the evaluated cell in their equations
        :return: None
        """
        for dependent_upon in all_dependent_on_cell:
            cell = self.workbook.get_cell(dependent_upon)
            self.evaluate(cell, cell.data)

    def _evaluate(self, data: str, location: Location) -> Tuple[str, Set[Location]]:
        """
        evaluate logic, firstly parse the equation and then calculate the equation
        :param data: raw input
        :param location: data cell location
        :return: [evaluation, dependencies]
        """
        if not data.startswith("="):
            return data, set()

        equation, _, cell_dependencies = self.equation_parser.parse(data[1:].upper(), location)
        try:
            evaluation = str(self.equation_evaluator.evaluate(equation))
        except EvaluationError as e:
            evaluation = f"Error:{e.message}"

        return evaluation, cell_dependencies

    def reload_dependency_tree(self) -> None:
        """
        just reload the dependency tree, for recreation of the hashes
        :return: None
        """
        self.dependency_manager.reload_tree()
