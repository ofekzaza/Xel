from typing import List
import openpyxl

from .base_importer import BaseImporter
from src.models.worksheet import Worksheet


class XlsxImporter(BaseImporter):
    """
    Import a xlsx file into a list of worksheet,
    support data and the formulas features.
    """
    def __init__(self) -> None:
        super().__init__("Xlsx")

    def import_sheets(self, path: str) -> List[Worksheet]:
        wb = openpyxl.load_workbook(path, data_only=False)
        sheets = []
        for sheet_name in wb.get_sheet_names():
            xl_sheet = wb.get_sheet_by_name(str(sheet_name))
            row_index = 0
            worksheet = Worksheet(name=str(sheet_name))
            for row in xl_sheet.rows:
                col_index = 0
                for xl_cell in row:
                    cell = worksheet.get_cell(col_index, row_index)
                    data = str(xl_cell.value) if xl_cell.value else ""
                    cell.set_data(data, data)
                    worksheet.set_cell(col_index, row_index, cell)
                    col_index += 1
                row_index += 1
            sheets.append(worksheet)
        return sheets
