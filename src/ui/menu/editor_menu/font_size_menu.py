import tkinter as tk
from tkinter import LEFT, RIGHT
from typing import Optional, Any

from tksheet import EventDataDict
from ttkwidgets.autocomplete import AutocompleteCombobox

from src.ui.gui_book import GuiBook


class FontSizeMenu(tk.Frame):
    def __init__(self, root: tk.Frame, gui_book: GuiBook, **kw: Any) -> None:
        super().__init__(root, **kw)
        self.gui_book = gui_book

        self.max_size = 48
        self.min_size = 10  # smaller than that the ui acts weird
        self.state = tk.StringVar()
        self.state.set("12")

        self.combobox = AutocompleteCombobox(
            self,
            completevalues=list(map(str, range(self.min_size, self.max_size + 1))),
            textvariable=self.state,
            width=5
        )
        self.combobox.bind('<<ComboboxSelected>>', self._update_font_size)
        self.combobox.bind("<Return>", self._update_font_size)
        self.combobox.pack(side=LEFT, pady=1, padx=1)

        self.increase_button = tk.Button(self, text="A^", command=self._increase_font_size)
        self.increase_button.pack(side=LEFT, padx=2)

        self.decrease_button = tk.Button(self, text="A▽", command=self._decrease_font_size)
        self.decrease_button.pack(side=RIGHT)

    def _increase_font_size(self, event: Optional[EventDataDict] = None) -> None:
        new_font_size = int(self.state.get())
        if new_font_size < self.max_size - 1:
            new_font_size += 2
        elif new_font_size == self.max_size - 1:
            new_font_size = self.max_size
        self.state.set(str(new_font_size))
        self._set_font_size(int(new_font_size))

    def _update_font_size(self, event: Optional[EventDataDict] = None) -> None:
        new_font_size = int(self.state.get())
        self._set_font_size(int(new_font_size))

    def _decrease_font_size(self, event: Optional[EventDataDict] = None) -> None:
        new_font_size = int(self.state.get())
        if new_font_size > self.min_size + 1:
            new_font_size -= 2
        elif new_font_size == self.min_size + 1:
            new_font_size = self.min_size
        self.state.set(str(new_font_size))
        self._set_font_size(int(new_font_size))

    def _set_font_size(self, font_size: int) -> None:
        if font_size in range(self.min_size, self.max_size + 1):
            for sheet in self.gui_book.sheets.values():
                sheet.set_font_size(font_size)
