from typing import Callable, Dict

from pydantic import BaseModel, PrivateAttr


class CellExternalProperties(BaseModel):
    """
    sub parameters of a cell,
    all the parameters of a cell which represents is outer appearance
    """
    color: str = "black"
    bg_color: str = "white"
    alignment: str = "left"

    def set_color(self, color: str) -> None:
        self.color = color

    def set_bg_color(self, bg_color: str) -> None:
        self.bg_color = bg_color

    def set_alignment(self, alignment: str) -> None:
        self.alignment = alignment
