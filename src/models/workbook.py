from typing import Dict, Any, Optional, Iterable

from pydantic import BaseModel, Field, PrivateAttr

from src.models.cell import Cell
from src.models.location import Location
from src.models.worksheet import Worksheet


class Workbook(BaseModel):
    """
    work book is exists only once within an application,
    contains several worksheets under it
    have a name
    and offers all worksheet management function under it, and to get a cell using a location object
    """
    name: str
    worksheets: Dict[str, Worksheet] = Field(default_factory=dict)
    _sheets_caps_to_origin: Dict[str, str] = PrivateAttr(default_factory=dict)

    def model_post_init(self, __context: Any) -> None:
        if not self.worksheets:
            self.create_default_worksheet() # create an empty worksheet if none exists

    def create_default_worksheet(self) -> Worksheet:
        return self.add_worksheet("Sheet1")

    def add_worksheet(self, name: str) -> Worksheet:
        """
        create a new worksheet
        :param name: name of the new worksheet
        :return: Worksheet
        """
        worksheet = Worksheet(name=name)
        self.worksheets[name] = worksheet
        self._sheets_caps_to_origin[name.upper()] = name
        return worksheet

    def overwrite_worksheet(self, worksheet: Worksheet) -> None:
        """
        :param worksheet: What to Upsert
        :return: None
        """
        self.worksheets[worksheet.name] = worksheet
        self._sheets_caps_to_origin[worksheet.name.upper()] = worksheet.name

    def rename_worksheet(self, original: str, new: str, dependencies: Iterable[Location]) -> None:
        """
        change name of existing worksheet
        plus changes the sheet name in all cells
        :param original: original sheet name
        :param new: new sheet name
        :param dependencies: cells which are dependent on cells from this sheet
        :return: None
        """
        dependent_cells = [self.get_cell(loc) for loc in dependencies]
        original = self._sheets_caps_to_origin[original.upper()]
        original_upper = original.upper()
        new_upper = new.upper()
        worksheet = self.worksheets[original]
        worksheet.name = new
        self._sheets_caps_to_origin[new_upper] = new
        self.worksheets[new] = worksheet
        del self.worksheets[original]
        del self._sheets_caps_to_origin[original_upper]

        for column in self.worksheets[new].columns:
            for cell in column.cells:
                cell.location.sheet = new

        for cell in dependent_cells:
            upper_data = cell.data.upper()
            if cell.data.startswith("=") and original_upper in upper_data:
                cell.set_data(cell.data.upper().replace(f"{original_upper}:", f"{new_upper}:"), cell.evaluation)

    def remove_worksheet(self, name: str) -> bool:
        """
        delete a worksheet from the books
        :param name: which sheet to remove
        :return: True if worksheet was remove False if it does not exists
        """
        if not self.get_worksheet(name, True):
            return False
        del self.worksheets[self._sheets_caps_to_origin[name.upper()]]
        return True

    def get_worksheet(self, name: str, caps: bool = False) -> Optional[Worksheet]:
        """
        :param name: base name
        :param caps: should search worksheet in caps
        :return: worksheet object if such exists with the requested name
        """
        if caps:
            return self.worksheets.get(self._sheets_caps_to_origin.get(name.upper(), ""), None)
        return self.worksheets.get(name)

    def get_cell(self, location: Location) -> Cell:
        """
        :param location: where the cell exists within the workbook
        :return: Cell
        """
        workbook = self.get_worksheet(location.sheet.upper(), True)
        if not workbook:
            raise ValueError("location worksheet doesnt exists")
        return workbook.get_cell(location.column, location.row)
