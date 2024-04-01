from functools import partial
from tkinter import BOTTOM, LEFT
from typing import Dict, Optional, Union, Any

import tkinter as tk

from src.auto_filler import AutoFillerFactory
from src.common import change_dict_key
from src.evaluator.evaluator import Evaluator
from src.models.workbook import Workbook
from src.models.worksheet import Worksheet
from src.ui.gui_sheet import GuiSheet
from src.ui.common import popup_input_window


class GuiBook(tk.Frame):
    """
    Graphical representation of the worksheet

    """

    def __init__(
            self,
            master: tk.Tk,
            workbook: Workbook,
            evaluator: Evaluator,
            auto_filler: AutoFillerFactory,
            **kw: Any
    ) -> None:
        super().__init__(master, **kw)
        self.auto_filler = auto_filler
        self.master: tk.Tk = master
        self.workbook = workbook
        self.evaluator = evaluator
        self.current_worksheet = list(self.workbook.worksheets.keys())[0]
        self.sheets: Dict[str, GuiSheet] = {}
        self.sheets_buttons: Dict[str, tk.Button] = {}

        self.sheets_management_frame = tk.Frame()
        self.new_sheet_text = tk.StringVar()

        for name in self.workbook.worksheets:
            self._load_sheet(name)

        self.sheets_management_frame.pack(side=BOTTOM)
        self.choose_sheet(self.current_worksheet)

    def create_sheet(self, caller: tk.Button) -> None:
        popup_input_window(self._validate_new_sheet_name, self._create_sheet, self.sheets_management_frame, caller)

    def _create_sheet(self, name: Optional[str] = None) -> None:
        """
        create a new empty gui sheet and worksheet
        :param name: worksheet name
        :return: None
        """
        if not name:
            name = self.new_sheet_text.get()
            if not self._validate_new_sheet_name(name):
                return  # do not create new sheet without a name, or already existing name
            self.new_sheet_text.set("")

        self.workbook.add_worksheet(name)
        self._load_sheet(name)
        self.choose_sheet(name)

    def _validate_new_sheet_name(self, name: Optional[str]) -> bool:
        return name is not None and len(name) > 0 and not self.workbook.get_worksheet(name)

    def _load_sheet(self, name: str) -> None:
        """
        load a sheet from the workbook to the ui
        :param name: sheet name
        """
        worksheet = self.workbook.get_worksheet(name)
        if not worksheet:
            raise IndexError("worksheet was not found")
        self.sheets[name] = GuiSheet(self, worksheet, self.evaluator, self.auto_filler)
        text = tk.StringVar()
        text.set(name)
        button = tk.Button(
            self.sheets_management_frame,
            textvariable=text,
            command=partial(self.choose_sheet, text),
            width=10
        )
        button.pack(side=LEFT)
        right_click_menu = self._create_sheets_management_menu(text, button)
        # Bind the right-click event to show the menu
        button.bind("<Button-3>", lambda e: right_click_menu.tk_popup(e.x_root, e.y_root))

        self.sheets_buttons[name] = button

    def _create_sheets_management_menu(self, text: tk.StringVar, button: tk.Button) -> tk.Menu:
        """
        create the right click menu of the worksheet,
        each worksheet button have his own management menu
        :param text: worksheet name
        :param button: worksheet button
        :return: Worksheets management menu
        """
        right_click_menu = tk.Menu(self.sheets_management_frame, tearoff=0)
        right_click_menu.add_command(label="Rename", command=lambda: self.rename_sheet(text))
        right_click_menu.add_command(label="Delete", command=lambda: self.delete_sheet(text))
        right_click_menu.add_command(label="Add", command=lambda: self.create_sheet(button))
        return right_click_menu

    def choose_sheet(self, sheet_name: Union[tk.StringVar, str]) -> None:
        """
        when pressing a sheet button, this method get called,
        and it changed the current shown gui sheet
        :param sheet_name: new sheet to display
        :return: None
        """
        if isinstance(sheet_name, tk.StringVar):
            sheet_name = sheet_name.get()

        for name, gui_sheet in self.sheets.items():
            if name != sheet_name:
                gui_sheet.pack_forget()
                self.sheets_buttons[name].configure(background='SystemButtonFace')

        self.sheets[sheet_name].pack(expand=True, fill='both')  # expand - 'yes'
        self.current_worksheet = sheet_name
        self.sheets_buttons[sheet_name].configure(background='lavender')

    def _rename_sheet_logic(self, sheet_text: tk.StringVar, new_name: str) -> None:
        """
        renames the worksheet, with the new name
        sheet_text will be updated to new name
        :param sheet_text: sheet name text var
        :param new_name: new name of the worksheet
        :return: None
        """
        original_name = str(sheet_text.get())
        dependencies = self.evaluator.dependency_manager.get_dependent_on_sheet(original_name)
        self.workbook.rename_worksheet(original_name, new_name, dependencies)
        change_dict_key(self.sheets, original_name, new_name)
        change_dict_key(self.sheets_buttons, original_name, new_name)
        sheet_text.set(new_name)

    def rename_sheet(self, sheet_name: tk.StringVar) -> None:
        """
        create popup which with input the renaming happens
        :param sheet_name: sheet name string var
        :return: None
        """
        popup_input_window(
            self._validate_new_sheet_name,
            partial(self._rename_sheet_logic, sheet_name),
            self.sheets_management_frame,
            self.sheets_buttons[sheet_name.get()]
        )

    def delete_sheet(self, name: Union[tk.StringVar, str]) -> None:
        """
        :param name:
        :return:
        """
        if isinstance(name, tk.StringVar):
            name = name.get()

        sheet = self.sheets[name]
        button = self.sheets_buttons[name]

        del self.sheets[name]
        del self.sheets_buttons[name]
        self.workbook.remove_worksheet(name)
        if not self.workbook.worksheets:
            # create an default sheet if all are deleted
            worksheet = self.workbook.create_default_worksheet()
            self._load_sheet(worksheet.name)
            self.choose_sheet(worksheet.name)
        elif self.current_worksheet == name:
            # show new sheet if the current one is deleted
            self.choose_sheet(list(self.workbook.worksheets.keys())[0])

        # do this last for safety
        sheet.destroy()
        button.destroy()

    def overwrite_worksheet(self, worksheet: Worksheet) -> None:
        """
        upsert (update or insert) a worksheet into the workbook
        create a temp sheet inorder to keep one sheet alive in the ui
        :param worksheet: what to upsert
        :return: None
        """
        TEMP_SHEET = "TEMPWORKSHEET"
        if self.workbook.get_worksheet(worksheet.name, True):
            self._create_sheet(TEMP_SHEET)
            self.delete_sheet(worksheet.name)
        self.workbook.overwrite_worksheet(worksheet)
        self._load_sheet(worksheet.name)
        self.choose_sheet(worksheet.name)
        if TEMP_SHEET in self.sheets:
            self.delete_sheet(TEMP_SHEET)

    def set_title(self, title: str) -> None:
        """
        update workbook title,
        changed the title of the application
        :param title: name for the workbook
        :return: None
        """
        self.workbook.name = title
        self.master.title(f"Xel Spreadsheet - {self.workbook.name}")

    def active_gui_sheet(self) -> GuiSheet:
        """

        :return: current opened gui sheet
        """
        return self.sheets[self.current_worksheet]
