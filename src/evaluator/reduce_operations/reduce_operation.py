from abc import ABC, abstractmethod
import re
from typing import List


class ReduceOperation(ABC):
    def __init__(self, name: str) -> None:
        self.name = name.upper()
        if not self.name:
            raise ValueError("Operation name is Empty")

        if not re.compile("[A-Z]+").fullmatch(self.name):
            raise ValueError("Operation name must be only upper letters")

    @abstractmethod
    def calculate(self, table: List[List[str]]) -> str:
        pass

    # @abstractmethod
    @property
    def documentation(self) -> str:
        return "default"
