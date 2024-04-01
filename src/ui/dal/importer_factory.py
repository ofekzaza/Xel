import os
from typing import Dict, Optional

from src.dal import IMPORTERS, BaseImporter
from src.ui.gui_book import GuiBook


class ImporterFactory:
    """
    Factory design patten for supported importers
    """
    def __init__(self) -> None:
        self.importers: Dict[str, BaseImporter] = {importer.name: importer for importer in IMPORTERS}

    def import_to(self, gui_book: GuiBook, path: str) -> Optional[str]:
        """
        import existing file from path to the gui book
        :param gui_book: gui of the workbook
        :param path: where to load file from
        :return: Error message
        """
        if not os.path.exists(path):
            return f"File path does not exist '{path}'"

        if os.path.isdir(path):
            return f"Path leads to a directory '{path}'"

        file_type = path.split(".")[-1]
        if file_type not in self.importers:
            return f"Cant import this file type '{file_type}'"

        new_sheets = self.importers[file_type].import_sheets(path)

        for sheet in new_sheets:
            gui_book.overwrite_worksheet(sheet)
        return None
