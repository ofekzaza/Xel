from typing import Optional, Callable, Any

# this lib does not have types library
from tksheet import Sheet, EventDataDict
from tkinter import BOTTOM
import tkinter as tk

from src.auto_filler import AutoFillerFactory
from src.common import index_to_letters
from src.evaluator.evaluator import Evaluator
from src.models.cell import Cell
from src.models.cell_external_properties import CellExternalProperties
from src.models.column import Column
from src.models.worksheet import Worksheet
from src.ui.gui_sheet.gui_sheet_auto_fillers import GuiSheetAutoFillers
from src.ui.gui_sheet.gui_sheet_misc import GuiSheetMisc


class GuiSheet(tk.Frame):
    """
    Gui Frame of a worksheet
    """

    def __init__(
            self,
            master: tk.Frame,
            worksheet: Worksheet,
            evaluator: Evaluator,
            auto_filler: AutoFillerFactory,
            **kw: Any
    ) -> None:
        super().__init__(master, **kw)
        self.evaluator: Evaluator = evaluator
        self.worksheet: Worksheet = worksheet
        self.auto_filler = auto_filler

        self.font = "Arial"
        self.font_size = 12
        self.font_annotation = "normal"

        self.current_properties = CellExternalProperties()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        table = self.worksheet.get_cells_table(10)
        # create an instance of Sheet()
        self.sheet = Sheet(
            # set the Sheets parent widget
            self,
            headers=[column.title for column in self.worksheet.columns],
            data=[[cell.evaluation for cell in row] for row in table],
            theme="light green",
            height=520,
            width=1000,
        )

        for col_index in range(len(worksheet.columns)):
            column = worksheet.get_column(col_index)
            self._sync_column(col_index, column)
        self.sheet.font((self.font, self.font_size, self.font_annotation))

        self.sync_font()

        self.binds()

        self.sheet.pack(expand='yes', fill='both', side=BOTTOM)

        # add sub-options
        self.misc = GuiSheetMisc(self, self.sheet, self.worksheet, self.binds)
        self.auto_fill_extension = GuiSheetAutoFillers(
            self,
            self.sheet,
            self.worksheet,
            self.auto_filler,
            self.evaluator
        )

    def binds(self) -> None:
        # enable various bindings
        self.sheet.enable_bindings("all", "edit_index", "edit_header", "begin_edit_cell", "end_edit_cell")
        self.sheet.bind("<<SheetModified>>", self.sheet_modified)

        self.sheet.extra_bindings("begin_edit_cell", self.begin_edit_cell)
        self.sheet.extra_bindings("end_edit_cell", self.end_edit_cell)

    def _sync_column(self, col_index: int, column: Column, row_start: int = 0, row_end: Optional[int] = None) -> None:
        self.sync_column_title(col_index)
        for row_index in range(row_start, column.size if row_end is None else row_end + 1):
            cell = column.get_cell(row_index, col_index, self.worksheet.name)
            cell.bind_set_data(self.update_cell)
            self.sync_cell_external_properties(cell)
            if cell.data.startswith("="):  # efficiency
                self.evaluator.evaluate(cell, cell.data)

    def begin_edit_cell(self, event: EventDataDict) -> str:
        row, col = event.loc
        cell = self.worksheet.get_cell(col, row)
        return cell.data

    def end_edit_cell(self, event: EventDataDict) -> str:
        row, col = event.loc
        cell = self.worksheet.get_cell(col, row)
        return cell.evaluation

    def sync_data(self, event: EventDataDict) -> Any:
        """
        sync the data of the cells, headers, index
        after every action on the ui
        to see the base for this design see tksheet doc.
        :param event:
        :return:
        """
        # print (event)
        if event.eventname.endswith("header"):
            headers = event['header'].keys() if event.get('header') else event['cells']['header']
            for column in headers:
                self.worksheet.get_column(column).title = self.sheet.MT._headers[column]
                self.sync_column_title(column)
                # yes, the library is stupid. this is what we get for doing ui in python
            return event.value
        elif event.eventname.endswith("index"):
            return event.value
        else:
            cells = event['table'].keys() if event.get('table') else event['cells']['table']
            for (row, col) in cells:
                new_data = str(self.sheet.get_cell_data(row, col))
                cell = self.worksheet.get_cell(col, row)
                self.sheet.header_font()
                cell.bind_set_data(self.update_cell)
                self.evaluator.evaluate(cell, new_data)
                self.worksheet.set_cell(col, row, cell)
            return event.value

    def sync_column_title(self, column: int) -> None:
        title = self.worksheet.get_column(column).title
        letter = index_to_letters(column + 1)
        if not title or title.strip().replace(" ", "") == letter:
            title = letter
        elif not title.startswith(f"{letter} - "):
            title = f"{letter} - {title}"
        self.worksheet.get_column(column).title = title
        self.sheet.set_header_data(title, column)

    def update_cell(self, cell: Cell) -> None:
        self.sheet.set_cell_data(cell.location.row, cell.location.column, cell.evaluation)

    def sheet_modified(self, event: Optional[EventDataDict] = None) -> None:
        """
        get called after every action in the gui sheet takes place
        so the guisheet and the worksheet will be synced
        :param event: EventDataDict
        :return: None
        """
        self.sync_deletes(event)
        self.sync_data(event)
        self.sync_additions(event)

    def sync_deletes(self, event: EventDataDict) -> None:
        """
        sync between delete events in the ui, and the models,
        so when in the ui something is deleted the models will be updated.
        :param event: EventDataDict
        :return: None
        """
        deleted_event = event.get("deleted")
        if not deleted_event:
            return

        all_cells = []
        deleted_rows = deleted_event.get("rows")
        if deleted_rows:
            for i in deleted_rows:
                all_cells += self.worksheet.delete_row(i)

        deleted_columns = deleted_event.get("columns")
        if deleted_columns:
            for i in deleted_columns:
                all_cells += self.worksheet.delete_column(i)

        for cell in set(all_cells):
            if cell.data.startswith("="):
                self.evaluator.evaluate(cell, cell.data)

    def sync_additions(self, event: EventDataDict) -> None:
        """
        sync rows and columns additions, when someone add a row/column this function get called
        :param event:
        :return:
        """
        added_event = event.get("added")
        if not added_event:
            return

        rows_table = added_event.get('rows').get("table")
        if rows_table:
            start_row = min(rows_table)
            end_row = max(rows_table)
            self.worksheet.add_rows(start_row, end_row)
            self.evaluator.reload_dependency_tree()
            for i in range(len(self.worksheet.columns)):
                self._sync_column(i, self.worksheet.columns[i], start_row, end_row)

        columns_table = added_event.get("columns", {}).get("table")
        if columns_table:
            start = min(columns_table)
            columns = self.worksheet.add_columns(start, max(columns_table))
            self.evaluator.reload_dependency_tree()
            for i in range(len(columns)):
                self._sync_column(i + start, columns[i])

    def sync_cell_external_properties(self, cell: Cell) -> None:
        """
        set the external properties of this cell in the ui according to input
        :param cell: What to sync based on
        :return: None
        """
        props = cell.external_properties
        # again the typing of tk.sheet if just playing annoying, it is a tuple and not Tuple[int, int] :\
        loc = (cell.location.row, cell.location.column)
        self.sheet[loc].bg = props.bg_color
        self.sheet[loc].fg = props.color
        self.sheet[loc].align(props.alignment)

    def _update_selected_cells(self, update_function: Callable[[Cell], None]) -> None:
        selected_cells = self.sheet.get_selected_cells()
        for (row, col) in selected_cells:
            cell = self.worksheet.get_cell(col, row)
            update_function(cell)
            self.sync_cell_external_properties(cell)

    # all this subsection is events that get called to update selected rows according to customization

    def set_background_color(self, color: str) -> None:
        self._update_selected_cells(lambda cell: cell.external_properties.set_bg_color(color))

    def set_foreground_color(self, color: str) -> None:
        self._update_selected_cells(lambda cell: cell.external_properties.set_color(color))

    def set_selected_alignment(self, alignment: str) -> None:
        self._update_selected_cells(lambda cell: cell.external_properties.set_alignment(alignment))

    def set_font(self, font: str) -> None:
        self.font = font
        self.sync_font()

    def set_font_size(self, font_size: int) -> None:
        self.font_size = font_size
        self.sync_font()

    def set_font_annotation(self, font_annotation: str) -> None:
        self.font_annotation = font_annotation
        self.sync_font()

    def sync_font(self) -> None:
        selected_cells = self.sheet.get_selected_cells()
        for (row, col) in selected_cells:
            self.sheet.deselect(row, col)
        self.sheet.font((self.font, self.font_size, self.font_annotation))
        for (row, col) in selected_cells:
            self.sheet.select_cell(row, col)
        self.sheet.refresh()
        for row in range(self.worksheet.rows_length()):
            self.sheet.set_index_data(row + 1, row)
