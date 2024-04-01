import xlsxwriter

from src.dal.exporters.base_exporter import BaseExporter
from src.models.workbook import Workbook
from src.models.worksheet import Worksheet


class XlsxExporter(BaseExporter):
    """
        Export current worksheet to an excel file.
        Full export of the data including equations, in all worksheets,
        most equations still work within excel.
        does not include external features.
    """
    def __init__(self) -> None:
        super().__init__("Xlsx")

    def _export(self, workbook: Workbook, current_worksheet: Worksheet, final_path: str) -> None:
        xlsx_workbook = xlsxwriter.Workbook(final_path)
        for sheet_name, worksheet in workbook.worksheets.items():
            xlsx_worksheet = xlsx_workbook.add_worksheet(sheet_name)
            for row in range(worksheet.rows_length()):
                for col in range(worksheet.columns_length()):
                    cell = worksheet.get_cell(col, row)
                    if cell.data != cell.evaluation:
                        xlsx_worksheet.write_formula(row, col, cell.data, None, cell.evaluation)
                    else:
                        xlsx_worksheet.write(row, col, cell.evaluation)
        xlsx_workbook.close()
