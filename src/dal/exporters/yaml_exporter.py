import yaml

from src.dal.exporters.base_exporter import BaseExporter
from src.models.workbook import Workbook
from src.models.worksheet import Worksheet


class YamlExporter(BaseExporter):
    """
   Export current worksheet to a yaml file.
   Full export of the workbook, does not lose data and cell features.
   Useful if you want to reload the data later.
   """

    def __init__(self) -> None:
        super().__init__("Yaml")

    def _export(self, workbook: Workbook, current_worksheet: Worksheet, final_path: str) -> None:
        with open(final_path, 'w') as f:
            workbook_dict = workbook.dict()
            f.write(yaml.dump(workbook_dict))
            f.flush()
