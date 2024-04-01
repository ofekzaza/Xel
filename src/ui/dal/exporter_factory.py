import os
from typing import Optional, Dict, List, Tuple

from src.dal import EXPORTERS, BaseExporter
from src.models.workbook import Workbook
from src.ui.gui_book import GuiBook


class ExporterFactory:
    """
    Factory design pattern to all supported exports
    """
    def __init__(self) -> None:
        self.exporters: Dict[str, BaseExporter] = {exporters.name: exporters for exporters in EXPORTERS}

    def export_to(self, workbook: Workbook, gui_book: GuiBook, path: str, override: bool = False) -> Optional[str]:
        """
        Save workbook to path
        choose exported based on path file type
        :param workbook: what to save
        :param gui_book: the ui of the workbook
        :param path: where to save
        :param override: save over file, if path is occupied
        :return: Error message if exists
        """
        if os.path.exists(path):
            if override:
                try:
                    os.remove(path)
                except Exception as e:
                    return f"Cant override file, probably open somewhere `{path}`"
            else:
                return f"File already exists '{path}'"

        if os.path.isdir(path):
            return f"No File name or type given '{path}'"

        file_type = path.split(".")[-1]
        if file_type not in self.exporters:
            return f"Cant export this file type '{file_type}'"

        worksheet = workbook.get_worksheet(gui_book.current_worksheet)
        if not worksheet:
            return "Error worksheet does not exist"

        return self.exporters[file_type].export(workbook, worksheet, path)

    def get_types(self) -> List[Tuple[str, str]]:
        return [(exporter.name, f".{exporter.name.lower()}") for exporter in self.exporters.values()]
