import re
from typing import Optional, Tuple, List

from src.common import letters_to_index
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.models.worksheet import Worksheet


def split_in_upper_parentheses(expr_input: str, by: str) -> List[str]:
    split_all = expr_input.split(by)
    right_split = []
    united = ""
    for split in split_all:
        if united:
            united += by + split
        else:
            united = split
        if united.count("(") == united.count(")"):
            right_split.append(united)
            united = ""
    return right_split


def find_closing_parentheses(expr: str, i: int, include_start: bool = False) -> int:
    count = 0 if include_start else 1
    for j in range(i, len(expr)):
        c = expr[j]
        if c == "(":
            count += 1
        if c == ")":
            count -= 1
        if count == 0:
            return j
    raise EvaluationError("No closing parenthesis")


def extract_word_location(word: str) -> Tuple[Optional[int], Optional[int]]:
    i = 0
    if not word:
        return None, None

    while i < len(word) and not word[i].isdigit():
        i += 1
    row = int(word[i:]) - 1 if len(word) > i else None
    if i:
        try:
            col = letters_to_index(word[:i]) - 1 if len(word) > i else letters_to_index(word) - 1
        except Exception as e:
            raise EvaluationError("BadPointer") from e
    else:
        col = None
    return row, col


def extract_number(expr: str) -> str:
    number: str = ""
    for digit in expr:
        if not digit.isdigit() and digit != ".":
            return number
        number += digit
    return number


def is_word_a_pointer(expr: str, i: int, first_part: str, second_part: str) -> bool:
    return (
            (
                    i + 1 == len(expr) or
                    not (
                            (re.compile("[A-Za-z0-9]+").fullmatch(expr[i + 1]) and not second_part)  # sheet name
                            or expr[i + 1].isdigit()  # next char is number
                            or re.compile("[A-Z]*").fullmatch(expr[i] + expr[i + 1])  # part of word
                            or expr[i + 1] == ":"  # allow another word
                    )
            )
            and (
                    (
                            (not not second_part)
                            or (
                                    (
                                        not not first_part
                                    ) and first_part[-1].isdigit()
                            )
                    )
                    and (i + 1 == len(expr) or ":" not in [expr[i + 1], expr[i]])
            )
    )


def normalize_table_pointer(
        start_row: Optional[int],
        start_col: Optional[int],
        end_row: Optional[int],
        end_col: Optional[int],
        worksheet: Worksheet
) -> Tuple[int, int, int, int]:
    if start_col is None:
        start_col = 0
    if end_col is None:
        end_col = worksheet.columns_length() - 1
    if start_row is None:
        start_row = 0
    if end_row is None:
        end_row = worksheet.rows_length() - 1

    start_row, end_row = min(start_row, end_row), max(start_row, end_row)
    start_col, end_col = min(start_col, end_col), max(start_col, end_col)

    return end_col, end_row, start_col, start_row
