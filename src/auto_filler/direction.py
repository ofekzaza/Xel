from enum import Enum


class Direction(Enum):
    """
    direction for auto fill logic,
    is chosen by the user in the ui
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
