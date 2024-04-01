import json

from src.dal.exporters.base_exporter import BaseExporter
from src.models.workbook import Workbook
from src.models.worksheet import Worksheet


class JsonExporter(BaseExporter):
    """
        Export current worksheet to a json file.
        Full export of the data, does not lose data.
        Useful if you want to reload the data later.
    """
    def __init__(self) -> None:
        super().__init__("Json")

    def _export(self, workbook: Workbook, current_worksheet: Worksheet, final_path: str) -> None:
        with open(final_path, 'w') as f:
            workbook_dict = workbook.dict()
            f.write(json.dumps(workbook_dict, ensure_ascii=False))
            f.flush()
