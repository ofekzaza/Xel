import tkinter as tk
from tkinter import LEFT
from typing import Optional, Any

from tksheet import EventDataDict
from ttkwidgets.autocomplete import AutocompleteCombobox

from src.ui.gui_book import GuiBook
from src.ui.menu.editor_menu.config import FONTS


class FontTypeMenu(tk.Frame):
    def __init__(self, root: tk.Frame, gui_book: GuiBook, **kw: Any) -> None:
        super().__init__(root, **kw)
        self.gui_book = gui_book
        self.state = tk.StringVar()
        self.state.set("Ariel")

        self.combobox = AutocompleteCombobox(
            self,
            completevalues=sorted(FONTS),
            textvariable=self.state,
            width=15
        )
        self.combobox.bind('<<ComboboxSelected>>', self._update_font_type)
        self.combobox.bind("<Return>", self._update_font_type)
        self.combobox.pack(side=LEFT)

    def _update_font_type(self, event: Optional[EventDataDict] = None) -> None:
        new_font = self.state.get()
        if new_font in FONTS:
            for sheet in self.gui_book.sheets.values():
                sheet.set_font(new_font)
