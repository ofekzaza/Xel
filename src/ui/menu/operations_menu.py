import tkinter as tk
from functools import partial
from tkinter import RAISED, LEFT, messagebox
from typing import Dict, Any

from src.ui.common.options_menu import OptionsMenu
from src.evaluator import REDUCE_OPERATIONS, ORDERED_PAIR_VALUES_OPERATIONS
from src.ui.gui_book import GuiBook


class OperationsMenu(tk.Frame):
    def __init__(self, root: tk.Frame, gui_book: GuiBook, **kw: Any) -> None:
        super().__init__(root, **kw)
        reduce_operations = {operation.name: operation.documentation for operation in REDUCE_OPERATIONS}
        self.reduce_menu = OptionsMenu(
            self,
            list(reduce_operations.keys()),
            partial(self._summon_documentation_window, reduce_operations),
            text="functions",
            relief=RAISED
        )
        self.reduce_menu.pack(anchor='n', side=LEFT, padx=4)

        operands = {operation.name: operation.documentation for operation in ORDERED_PAIR_VALUES_OPERATIONS}
        self.pair_value_menu = OptionsMenu(
            self,
            list(operands.keys()),
            partial(self._summon_documentation_window, operands),
            text="operands",
            relief=RAISED
        )
        self.pair_value_menu.pack(anchor='n', side=LEFT, padx=4)

    def _summon_documentation_window(self, options: Dict[str, str], chosen: str) -> None:
        messagebox.showinfo(master=self, title=F"{chosen} Documentation", message=options[chosen])
