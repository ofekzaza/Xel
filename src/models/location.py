import uuid

from pydantic import BaseModel, PrivateAttr


class Location(BaseModel):
    """
    path to a cell in the workbook
    for each cell the location is uniquely and when the cell changed position,
    the location stays the same and his values are updated
    """
    row: int
    column: int
    sheet: str
    _id = PrivateAttr(default_factory=uuid.uuid4)

    def __hash__(self) -> int:
        return hash(self._id)
