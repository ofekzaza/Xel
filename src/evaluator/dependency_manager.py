from collections import defaultdict
from typing import Set, Dict, List

from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.models.location import Location


class DependencyManager:
    """
    Manage dependencies between cells
    which cells use which cells,
    keep two directions tree, so it can tell in O(1) from a cell location which cells uses him and which cells he uses.
    """
    def __init__(self) -> None:
        self.dependency_tree: Dict[Location, Set[Location]] = defaultdict(set)
        self.dependent_upon_tree: Dict[Location, Set[Location]] = defaultdict(set)

    def update_dependencies(self, loc: Location, cell_dependencies: Set[Location]) -> Set[Location]:
        for dependent_upon in self.dependency_tree[loc] - cell_dependencies:
            self.dependent_upon_tree[dependent_upon].remove(loc)
        self.dependency_tree[loc] = cell_dependencies
        for dependent_upon in cell_dependencies:
            self.dependent_upon_tree[dependent_upon].add(loc)
        return self.get_all_dependent_on_cell(loc)

    def get_all_dependent_on_cell(self, loc: Location) -> Set[Location]:
        return self._get_all_dependent_on_cell(loc, loc)

    def _get_all_dependent_on_cell(self, current: Location, origin: Location) -> Set[Location]:
        layer = self.dependent_upon_tree[current]
        if not layer:
            return set()
        if origin in layer or current in layer:
            raise EvaluationError("Cells are dependent on each other")

        children: Set[Location] = set()
        for new in layer:
            children.update(self._get_all_dependent_on_cell(new, origin))
        return children.union(layer)

    def reload_tree(self) -> None:
        new_tree_upon = defaultdict(set)
        new_tree = defaultdict(set)
        for key, value in self.dependent_upon_tree.items():
            new_tree_upon[key] = set(value)
        self.dependent_upon_tree = new_tree_upon
        for key, value in self.dependency_tree.items():
            new_tree[key] = set(value)
        self.dependency_tree = new_tree

    def get_dependent_on_sheet(self, sheet_name: str) -> List[Location]:
        dependent_on_sheet = []
        for loc, dependencies in self.dependency_tree.items():
            for dependency_location in dependencies:
                if dependency_location.sheet == sheet_name:
                    dependent_on_sheet.append(loc)
                    break
        return dependent_on_sheet
