from pydantic import BaseModel


class CellData(BaseModel):
    """
    only the data part of the cell, is used for predictions,
    auto filler returns cell data and not a cell, a cell is created only inside the workbook
    """
    data: str
    evaluation: str
