from abc import ABC, abstractmethod
import os
from typing import Optional

from src.models.workbook import Workbook
from src.models.worksheet import Worksheet


class BaseExporter(ABC):
    def __init__(self, name: str, workbook_exporter: bool = True) -> None:
        self.name = name.lower()
        self.workbook_exporter = workbook_exporter

    def export(self, workbook: Workbook, current_worksheet: Worksheet, path: str) -> Optional[str]:
        if os.path.isdir(path):
            return "path is directory"

        if os.path.exists(path):
            return "file already exists, please change path"

        try:
            self._export(workbook, current_worksheet, path)
            return None

        except Exception as e:
            return f"Failed exporting data to {path}, in type {self.name}"

    @abstractmethod
    def _export(self, workbook: Workbook, current_worksheet: Worksheet, final_path: str) -> None:
        pass
