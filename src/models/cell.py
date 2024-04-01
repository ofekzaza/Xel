from typing import Callable, Optional

from pydantic import BaseModel, PrivateAttr

from src.models.cell_external_properties import CellExternalProperties
from src.models.location import Location


class Cell(BaseModel):
    """
    Cell model
    have a location where exists in the workbook
    data what the user entered
    evaluation the result of the formula
    external properties how the cell looks
    _update_event - a function to call when the data is updated
    """
    location: Location
    data: str = ""
    evaluation: str = ""
    external_properties: CellExternalProperties = CellExternalProperties()
    _update_event: Optional[Callable[["Cell"], None]] = PrivateAttr(default=None)

    def set_data(self, data: str, evaluation: str) -> str:
        self.data = data
        self.evaluation = evaluation
        if self._update_event:
            self._update_event(self)
        return self.evaluation

    def bind_set_data(self, update_function: Callable[["Cell"], None]) -> None:
        self._update_event = update_function

    def __hash__(self) -> int:
        return hash(self.location)
