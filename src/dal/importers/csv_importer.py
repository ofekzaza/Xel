import csv
from typing import List

from .base_importer import BaseImporter
from src.models.worksheet import Worksheet


class CsvImporter(BaseImporter):
    """
    Csv importer, loads a csv file into one worksheet,
    loads only the evaluations, does not support anything else
    """
    def __init__(self) -> None:
        super().__init__("Csv")

    def import_sheets(self, path: str) -> List[Worksheet]:
        with open(path, 'r') as f:
            reader = csv.reader(f)
            worksheet = Worksheet(name=path.split("/")[-1].split(".")[0])
            row_index = 0
            for row in reader:
                col_index = 0
                for cell_data in row:
                    cell = worksheet.get_cell(col_index, row_index)
                    cell.set_data(cell_data, cell_data)
                    worksheet.set_cell(col_index, row_index, cell)
                    col_index += 1
                row_index += 1
            return [worksheet]
