from collections import defaultdict
from functools import partial
from typing import List, Optional, Tuple, Dict

import tkinter as tk
from tksheet import Sheet

from src.auto_filler import Direction, AutoFillerFactory
from src.auto_filler.cell_data import CellData
from src.common import safe_int
from src.evaluator import Evaluator
from src.models.cell import Cell
from src.models.worksheet import Worksheet
from src.ui.common import popup_input_window


class GuiSheetAutoFillers:
    """
       GuiSheetAutoFillers, add right click options for autofillers
       connect the autofiller factory with the gui.

    """

    def __init__(
            self,
            root: tk.Frame,
            sheet: Sheet,
            worksheet: Worksheet,
            auto_filler:
            AutoFillerFactory,
            evaluator: Evaluator
    ) -> None:
        self.root = root
        self.sheet = sheet
        self.worksheet = worksheet
        self.auto_filler = auto_filler
        self.evaluator = evaluator

        self.sheet.popup_menu_add_command(
            "AutoFill Right",
            partial(self.auto_fill, Direction.RIGHT),
            table_menu=True,
            header_menu=False,
            empty_space_menu=False,
            index_menu=False,
        )

        self.sheet.popup_menu_add_command(
            "AutoFill Down",
            partial(self.auto_fill, Direction.DOWN),
            table_menu=True,
            header_menu=False,
            empty_space_menu=False,
            index_menu=False,
        )

        self.sheet.popup_menu_add_command(
            "AutoFill Left",
            partial(self.auto_fill, Direction.LEFT),
            table_menu=True,
            header_menu=False,
            empty_space_menu=False,
            index_menu=False,
        )

        self.sheet.popup_menu_add_command(
            "AutoFill Up",
            partial(self.auto_fill, Direction.UP),
            table_menu=True,
            header_menu=False,
            empty_space_menu=False,
            index_menu=False,
        )

    def auto_fill(self, direction: Direction) -> None:
        """
        call the autofill logic from the ui
        :param direction: direction of the autofill
        :return: None
        """
        popup_input_window(
            self._validate_input,
            partial(self._auto_fill_cells, direction),
            self.root,
            self.root,
            background_text="Length of Autofill"
        )

    def _validate_input(self, data: str) -> bool:
        parsed = safe_int(data)
        return isinstance(parsed, int) and parsed > 0

    def get_selected_table(self) -> List[List[Cell]]:
        """
        :return: selected cells as table of row, col, cell
        """
        selected_cells = self.sheet.get_selected_cells()
        dict_table: Dict[str, Dict[str, Optional[Cell]]] = defaultdict(lambda: defaultdict(None))
        for (row, col) in selected_cells:
            dict_table[row][col] = self.worksheet.get_cell(col, row)

        table = []
        for row_index in sorted(dict_table.keys()):
            table_row = []
            for col_index in sorted(dict_table[row_index].keys()):
                cell = dict_table[row_index][col_index]
                if not cell:
                    raise ValueError("Prediction cell is empty, Happens if selected area is not squared")
                table_row.append(cell)
            table.append(table_row)
        return table

    def _auto_fill_cells(self, direction: Direction, length: int) -> None:
        """
        call auto fill logic, and update results in workbook
        :param direction: which way to autofill
        :param length: how many cells to predict
        :return: None
        """
        length = int(length)  # just to make sure
        table = self.get_selected_table()
        if not table:
            return None

        predictions = self.auto_filler.auto_fill(table, length, direction)
        if not predictions:
            return None

        cells = self._set_cell_data_to_prediction(direction, length, predictions, table)

        for cell in cells:
            self.evaluator.evaluate(cell, cell.data)

    def _set_cell_data_to_prediction(
            self,
            direction: Direction,
            length: int,
            predictions: List[List[CellData]],
            table: List[List[Cell]]
    ) -> List[Cell]:
        """
        take autofill prediction and update the relevant cells to the prediction
        :param direction:
        :param length:
        :param predictions: prediction table
        :param table: selected cells
        :return: updated cells
        """
        cells = []
        for row_index in range(len(predictions)):
            for col_index in range(len(predictions[row_index])):
                row, col = self._get_prediction_location(row_index, col_index, table, length, direction)
                if col < 0 or row < 0 or col >= self.worksheet.columns_length() or row >= self.worksheet.rows_length():
                    continue  # prediction is out of the table

                cell = self.worksheet.get_cell(col, row)
                prediction = predictions[row_index][col_index]
                cell.set_data(prediction.data, prediction.evaluation)
                cells.append(cell)
        return cells

    def _get_prediction_location(
            self,
            row_index: int,
            col_index: int,
            table: List[List[Cell]],
            length: int,
            direction: Direction
    ) -> Tuple[int, int]:
        """
        connect between prediction and specific cell
        :param row_index:
        :param col_index:
        :param table: selected cells
        :param length:
        :param direction:
        :return: row, col of cell from prediction
        """
        if direction == Direction.DOWN:
            base_loc = table[-1][col_index].location
            return base_loc.row + row_index + 1, base_loc.column

        if direction == Direction.UP:
            base_loc = table[0][col_index].location
            return base_loc.row + row_index - length, base_loc.column

        if direction == Direction.RIGHT:
            base_loc = table[row_index][-1].location
            return base_loc.row, base_loc.column + 1 + col_index

        if direction == Direction.LEFT:
            base_loc = table[row_index][-1].location
            return base_loc.row, base_loc.column - length + col_index

        raise IndexError("Unknown direction")
