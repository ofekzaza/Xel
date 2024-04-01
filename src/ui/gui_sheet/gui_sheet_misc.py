import tkinter as tk
from typing import Callable, Optional

from tksheet import Sheet, EventDataDict

from src.models.worksheet import Worksheet
from src.ui.common import popup_input_window


class GuiSheetMisc:
    """
    add Misc functionality to gui sheet
    such:
        - hide/display row/column
        - Insert/Delete row/column
        - Append rows/columns
    the module is separated from the main guisheet for clearer code.
    """

    def __init__(self, root: tk.Frame, sheet: Sheet, worksheet: Worksheet, binds: Callable[[], None]) -> None:
        self.root = root
        self.sheet = sheet
        self.worksheet = worksheet
        self.binds = binds

        self.sheet.popup_menu_add_command(
            "Hide Row",
            self.hide_rows,
            table_menu=False,
            header_menu=False,
            empty_space_menu=False,
        )

        self.sheet.popup_menu_add_command(
            "Show All Rows",
            self.show_rows,
            table_menu=False,
            header_menu=False,
            empty_space_menu=False,
        )

        self.sheet.popup_menu_add_command(
            "Hide Column",
            self.hide_columns,
            table_menu=False,
            index_menu=False,
            empty_space_menu=False,
        )

        self.sheet.popup_menu_add_command(
            "Show All Columns",
            self.show_columns,
            table_menu=False,
            index_menu=False,
            empty_space_menu=False,
        )

        self.sheet.popup_menu_add_command(
            "Append Rows",
            self.append_rows
        ),

        self.sheet.popup_menu_add_command(
            "Append Columns",
            self.append_columns,
        )

    def _append_rows(self, amount: str) -> None:
        i = int(amount)
        self.sheet.insert_rows(i, self.worksheet.rows_length())
        self.binds()

    def append_rows(self) -> None:
        popup_input_window(lambda x: x.isdigit(), self._append_rows, self.root, self.root, "10", "Insert Number")

    def _append_columns(self, amount: str) -> None:
        i = int(amount)
        self.sheet.insert_columns(i, self.worksheet.columns_length())
        self.binds()

    def append_columns(self) -> None:
        popup_input_window(lambda x: x.isdigit(), self._append_columns, self.root, self.root, "10", "Insert Number")

    def hide_rows(self, event: Optional[EventDataDict] = None) -> None:
        rows = self.sheet.get_selected_rows()
        if rows:
            self.sheet.hide_rows(rows)

    def show_rows(self, event: Optional[EventDataDict] = None) -> None:
        self.sheet.display_rows("all", redraw=True)

    def hide_columns(self, event: Optional[EventDataDict] = None) -> None:
        columns = self.sheet.get_selected_columns()
        if columns:
            self.sheet.hide_columns(columns)

    def show_columns(self, event: Optional[EventDataDict] = None) -> None:
        self.sheet.display_columns("all", redraw=True)
