from tkinter import TOP

import tkinter as tk

from src.auto_filler import AutoFillerFactory
from src.evaluator import Evaluator, REDUCE_OPERATIONS, ORDERED_PAIR_VALUES_OPERATIONS
from src.models.workbook import Workbook
from src.ui.gui_book import GuiBook
from src.ui.menu import GuiMenu


class Gui(tk.Tk):
    """
    Main class of Xel,
    works as bootstrapper and ui initiator
    """
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.workbook = Workbook(name="Starting workbook")
        self.title(f"Xel Spreadsheet - {self.workbook.name}")
        self.evaluator: Evaluator = Evaluator(self.workbook, ORDERED_PAIR_VALUES_OPERATIONS, REDUCE_OPERATIONS)
        self.auto_filler: AutoFillerFactory = AutoFillerFactory()
        self.gui_book: GuiBook = GuiBook(self, self.workbook, self.evaluator, self.auto_filler)

        self.gui_menu = GuiMenu(self, self.workbook, self.gui_book)
        self.gui_menu.pack(side=TOP, anchor='nw', pady=2)
        self.gui_book.pack(expand=True, fill='both')

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def run(self) -> None:
        """
        run xel using tkinter
        :return: None
        """
        self.mainloop()
