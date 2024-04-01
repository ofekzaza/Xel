from abc import ABC, abstractmethod
import re


class PairValuesOperation(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        if not self.name:
            raise ValueError("Operation name is Empty")

        if len(self.name) > 2:
            raise ValueError("Pair value operation name can be max two chars")

        if re.compile("[A-Za-z0-9]+").fullmatch(self.name):
            raise ValueError("Operation name contain letters or numbers")

    @abstractmethod
    def calculate(self, first: str, second: str) -> str:
        pass

    @property
    @abstractmethod
    def documentation(self) -> str:
        pass
