from abc import ABC, abstractmethod
from typing import List

from src.models.worksheet import Worksheet


class BaseImporter(ABC):
    def __init__(self, name: str) -> None:
        self.name = name.lower()

    @abstractmethod
    def import_sheets(self, path: str) -> List[Worksheet]:
        pass
