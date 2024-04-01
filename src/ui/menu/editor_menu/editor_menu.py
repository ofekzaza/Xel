import tkinter as tk
from tkinter import RAISED, LEFT
from typing import Any

from src.ui.gui_book import GuiBook
from src.ui.common.options_menu import OptionsMenu
from src.ui.menu.editor_menu.config.colors_config import COLORS
from src.ui.menu.editor_menu.font_size_menu import FontSizeMenu
from src.ui.menu.editor_menu.font_type_menu import FontTypeMenu


class EditorMenu(tk.Frame):
    def __init__(self, master: tk.Frame, gui_book: GuiBook, **kw: Any) -> None:
        super().__init__(master, **kw)
        self.gui_book = gui_book
        self.font_type_frame = FontTypeMenu(self, gui_book)
        self.font_type_frame.pack(side=LEFT, padx=4, pady=1)
        self.font_size_frame = FontSizeMenu(self, gui_book)
        self.font_size_frame.pack(side=LEFT, padx=4)
        self.font_annotation_menu = OptionsMenu(
            self,
            ["normal", "bold", "italic"],
            self._update_font_annotation,
            text="font annotation",
            relief=RAISED
        )
        self.font_annotation_menu.pack(side=LEFT)

        self.font_color = OptionsMenu(
            self,
            COLORS,
            self.update_font_color,
            text="font color",
            relief=RAISED,
            are_options_colors=True
        )
        self.font_color.pack(anchor='n', side=LEFT, padx=4)
        self.background_color = OptionsMenu(
            self,
            COLORS,
            self.update_bg_color,
            text="background color",
            relief=RAISED,
            are_options_colors=True
        )
        self.background_color.pack(anchor='n', side=LEFT, padx=4)

        self.alignments_menu = OptionsMenu(
            self,
            ["left", "center", "right"],
            self.update_cell_alignment,
            text="alignment",
            relief=RAISED
        )
        self.alignments_menu.pack(anchor='n', side=LEFT, padx=4)

    def update_cell_alignment(self, alignment: str) -> None:
        self.gui_book.active_gui_sheet().set_selected_alignment(alignment)

    def update_font_color(self, color: str) -> None:
        self.gui_book.active_gui_sheet().set_foreground_color(color)

    def update_bg_color(self, color: str) -> None:
        self.gui_book.active_gui_sheet().set_background_color(color)

    def _update_font_annotation(self, annotation: str) -> None:
        for sheet in self.gui_book.sheets.values():
            sheet.set_font_annotation(annotation)
