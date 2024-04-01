import itertools
from typing import Union, Any

from openpyxl.utils.cell import get_column_letter, column_index_from_string


def index_to_letters(num: int) -> str:
    return get_column_letter(num)


def letters_to_index(letters: str) -> int:
    return column_index_from_string(letters)


def is_index(word: str) -> bool:
    try:
        letters_to_index(word)
        return True
    except Exception:
        return False


def change_dict_key(dictionary: dict[Any, Any], original: object, new: object) -> None:
    data = dictionary[original]
    dictionary[new] = data
    del dictionary[original]


def safe_float(string: str) -> Union[float, str]:
    try:
        return float(string)
    except Exception as e:
        return str(string)


def safe_int(string: str) -> Union[int, str]:
    try:
        return int(safe_float(string))
    except Exception as e:
        return str(string)


def pivot_table(table: list[list[Any]], default_value: object = None) -> list[list[Any]]:
    return list(map(list, itertools.zip_longest(*table, fillvalue=default_value)))
