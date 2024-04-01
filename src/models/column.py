from typing import List, Any, Optional

from pydantic import BaseModel, Field

from src.models.cell import Cell
from src.models.location import Location


class Column(BaseModel):
    """
    A column of cells
    have a title which is a header in the worksheet
    """
    title: str = ""
    cells: List[Cell] = Field(default_factory=list)
    size: int = 0

    def model_post_init(self, __context: Any) -> None:
        self.size = len(self.cells)

    def get_cell(self, index: int, column: Optional[int] = None, sheet: Optional[str] = None) -> Cell:
        if len(self.cells) > index:
            return self.cells[index]
        if column is not None and sheet:
            cell = self._generate_cell(column, index, sheet)
            self.set_cell(index, cell)
            return cell
        raise IndexError("Cell was not found")

    def _generate_cell(self, column: int, row: int, sheet: str) -> Cell:
        return Cell(location=Location(row=row, column=column, sheet=sheet))

    def set_cell(self, number: int, cell: Cell) -> None:
        for row in range(len(self.cells), number + 1):
            self.cells.append(self._generate_cell(cell.location.column, row, cell.location.sheet))

        self.cells[number] = cell

        if number + 1 > self.size:
            self.size = number + 1

    def delete_row(self, index: int) -> List[Cell]:
        if index >= len(self.cells):
            return []

        del self.cells[index]
        for cell in self.cells[index:]:
            cell.location.row -= 1
        return self.cells[index:]

    def update_column_index(self, index: int) -> None:
        for cell in self.cells:
            cell.location.column = index

    def add_rows(self, sheet: str, col_index: int, start: int, end: int) -> List[Cell]:
        new_rows = [self._generate_cell(col_index, i, sheet) for i in range(start, end + 1)]
        moved_rows = self.cells[start:]
        for i in range(len(moved_rows)):
            moved_rows[i].location.row = end + i + 1
        self.cells = self.cells[:start] + new_rows + moved_rows
        return new_rows
