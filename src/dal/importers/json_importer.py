import json
from typing import List

from .base_importer import BaseImporter
from src.models.workbook import Workbook
from src.models.worksheet import Worksheet


class JsonImporter(BaseImporter):
    """
    Import a json file into a list of worksheet,
    support all features.
    """
    def __init__(self) -> None:
        super().__init__("Json")

    def import_sheets(self, path: str) -> List[Worksheet]:
        with open(path, 'r') as f:
            dict_data = json.loads(f.read())
            workbook = Workbook.model_validate(dict_data)
            return list(workbook.worksheets.values())
