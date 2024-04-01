import tkinter as tk
from tkinter import RAISED, LEFT
from typing import Union, Any

from src.models.workbook import Workbook
from src.ui.gui_book import GuiBook
from src.ui.menu.editor_menu import EditorMenu
from src.ui.menu.file_menu import FileMenuButton
from src.ui.menu.operations_menu import OperationsMenu


class GuiMenu(tk.Frame):
    def __init__(self, master: tk.Tk, workbook: Workbook, gui_book: GuiBook, **kw: Any) -> None:
        super().__init__(master, **kw)
        self.workbook = workbook
        self.gui_book = gui_book
        self.file_menu = FileMenuButton(self, workbook, gui_book, text="file", relief=RAISED)
        self.file_menu.pack(anchor='n', side=LEFT)
        self.editor_menu = EditorMenu(self, gui_book=gui_book, relief=RAISED)
        self.editor_menu.pack(anchor='n', padx=4, side=LEFT)
        self.operations_menu = OperationsMenu(self, gui_book=gui_book, relief=RAISED)
        self.operations_menu.pack(anchor='n', padx=4, side=LEFT)
