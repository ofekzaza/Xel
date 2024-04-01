import csv

from src.dal.exporters.base_exporter import BaseExporter
from src.models.workbook import Workbook
from src.models.worksheet import Worksheet


class CsvExporter(BaseExporter):
    """
        Export current worksheet to csv.
        Does not export all the workbook because csv supports only one worksheet.
        Export only the cell evaluation and nothing more.
    """
    def __init__(self) -> None:
        super().__init__("Csv", False)

    def _export(self, workbook: Workbook, current_worksheet: Worksheet, final_path: str) -> None:
        with open(final_path, 'w') as f:
            writer = csv.writer(f)
            for row_index in range(current_worksheet.rows_length()):
                row = []
                for col_index in range(len(current_worksheet.columns)):
                    row.append(current_worksheet.get_cell(col_index, row_index).data)
                writer.writerow(row)

            f.flush()
