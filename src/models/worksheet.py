from typing import List

from pydantic import BaseModel, Field

from src.common import letters_to_index
from src.models.column import Column
from src.models.cell import Cell


class Worksheet(BaseModel):
    """
    Xel model for a table of cells
    offer all table managements functions
    """
    name: str
    columns: list[Column] = Field(default_factory=list)

    def get_column_letters(self, letters: str) -> Column:
        """
        :param letters: Example: A1, G6
        :return: letters index in numbers
        """
        return self.get_column(letters_to_index(letters))

    def get_column(self, index: int) -> Column:
        while index >= len(self.columns):
            self.columns.append(Column())

        return self.columns[index]

    def get_cell(self, column: int, row: int) -> Cell:
        """

        :param column:
        :param row:
        :return: Cell
        """
        return self.get_column(column).get_cell(row, column, self.name)

    def set_cell(self, column: int, row: int, cell: Cell) -> None:
        """
        :param column: col to upsert
        :param row: row to upsert
        :param cell: cell to upsert
        :return: None
        """
        self.get_column(column).set_cell(row, cell)

    def columns_length(self) -> int:
        """
        :return: amount of columns in sheet
        """
        return len(self.columns)

    def rows_length(self) -> int:
        """
        :return: rows amount in the sheet
        """
        return max(map(lambda column: column.size, self.columns), default=0)

    def get_cells_table(self, min_size: int = 0) -> List[List[Cell]]:
        """
        if sheet does not contain min_size cols/row than it creates them
        :param min_size: min cols\rows to return
        :return: list of lists of the sheet cells
        """
        rows_size = self.rows_length()
        if rows_size < min_size:
            rows_size = min_size
        cols_size = len(self.columns) if len(self.columns) > min_size else min_size
        table = []
        for row_index in range(rows_size):
            row = []
            for col_index in range(cols_size):
                row.append(self.get_cell(col_index, row_index))
            table.append(row)
        return table

    def delete_row(self, index: int) -> List[Cell]:
        """
        delete a row from the sheet
        :param index: row to delete
        :return: list of deleted cells
        """
        if index >= self.rows_length():
            return []

        cells = []
        for column in self.columns:
            cells += column.delete_row(index)
        return cells

    def delete_column(self, index: int) -> List[Cell]:
        """
        remove a column for the sheet
        :param index: which column to remove from the sheet
        :return: cells of the removed column
        """
        if index >= len(self.columns):
            return []

        del self.columns[index]
        cells = []
        for column in self.columns[index:]:
            for cell in column.cells:
                cell.location.column -= 1
            cells += column.cells
        return cells

    def add_columns(self, start: int, end: int) -> List[Column]:
        """
        create new columns inside the table
        :param start: index of start
        :param end: index to end
        :return: list of newly created columns
        """
        new_columns = [Column() for i in range(start, end + 1)]
        moved_columns = self.columns[start:]
        for i in range(len(moved_columns)):
            moved_columns[i].update_column_index(end + i + 1)
        self.columns = self.columns[:start] + new_columns + moved_columns
        return new_columns

    def add_rows(self, start: int, end: int) -> None:
        """
        create new rows inside the table
        :param start: index of start
        :param end: index to end
        :return: None
        """
        for col_index in range(len(self.columns)):
            self.columns[col_index].add_rows(self.name, col_index, start, end)
