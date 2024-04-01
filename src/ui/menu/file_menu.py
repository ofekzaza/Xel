import webbrowser
from functools import partial
from tkinter import messagebox, filedialog
import tkinter as tk
from typing import Any

from src.models.workbook import Workbook
from src.ui.dal import ImporterFactory, ExporterFactory
from src.ui.gui_book import GuiBook


class FileMenuButton(tk.Menubutton):
    def __init__(self, master: tk.Frame, workbook: Workbook, gui_book: GuiBook, **kw: Any) -> None:
        super().__init__(master, **kw)
        self.master = master
        self.workbook = workbook
        self.gui_book = gui_book

        self._importer_factory = ImporterFactory()
        self._exporter_factory = ExporterFactory()
        self._export_path = ""
        self._import_path = ""
        self._save_path = ""

        self.menu = tk.Menu(self, tearoff=0)
        self["menu"] = self.menu
        self.menu.add_command(label="save", command=self.save)
        self.menu.add_command(label="import from", command=self.import_workbook)
        self.menu.add_command(label="export to", command=self.export_workbook)
        self.menu.add_command(label="Xel Video",
                              command=partial(webbrowser.open, "https://www.youtube.com/watch?v=9irQiFHmTjY"))
        self.menu.add_command(label="Excel Trailer",
                              command=partial(webbrowser.open, "https://www.youtube.com/watch?v=kOO31qFmi9A&t=1s"))

    def save(self) -> None:
        if not self._save_path:
            return self.export_workbook()

        error = self._exporter_factory.export_to(self.workbook, self.gui_book, self._save_path, True)
        if error:
            messagebox.showerror("Save failed", error)

    def import_workbook(self) -> None:
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        error = self._importer_factory.import_to(self.gui_book, file_path)
        if error:
            messagebox.showerror("Import failed", error)

        self._import_path = file_path
        if not self._export_path:
            self._save_path = file_path
            self.gui_book.set_title(file_path)

    def export_workbook(self) -> None:
        file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=self._exporter_factory.get_types())
        if not file_path:
            return None

        error = self._exporter_factory.export_to(self.workbook, self.gui_book, file_path, True)
        if error:
            messagebox.showerror("Export failed", error)
        self._export_path = file_path
        if self._save_path != file_path:
            self._save_path = file_path
            self.gui_book.set_title(file_path)
        return None
