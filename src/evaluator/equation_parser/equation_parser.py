from typing import Tuple, Set, Union, Any

from .common import \
    extract_number, \
    find_closing_parentheses, \
    extract_word_location, \
    is_word_a_pointer, \
    normalize_table_pointer, \
    split_in_upper_parentheses
from src.evaluator.exceptions.evaluation_error import EvaluationError
from src.models.location import Location
from src.models.workbook import Workbook
from src.common import safe_float


def _append_to_words(
        c: str,
        first_part: str,
        second_part: str,
        third_part: str,
        word: str
) -> Tuple[str, str, str, str]:
    if c == ":":
        pass
    elif third_part or second_part and word[-1] == ":":
        third_part += c
    elif second_part or first_part and word[-1] == ":":
        second_part += c
    else:
        first_part += c
    return word + c, first_part, second_part, third_part


class EquationParser:
    """
    Knows to take on word and parse it into a tree of the equation
    """

    def __init__(self, workbook: Workbook, pair_operations: Set[str], reduce_operations: Set[str]) -> None:
        self.reduce_operations = reduce_operations
        self.pair_operations = pair_operations
        self.workbook = workbook

    def parse(self, expr: str, location: Location) -> Tuple[list[Any], int, Set[Location]]:
        """
        Parses the expression into a list of numbers, operators, and function calls.
        """
        stack: list[Any] = []
        i = 0
        dependencies: Set[Location] = set()
        expr = expr.replace(" ", "")
        while i < len(expr):
            i = self._parse_one_word(expr, i, stack, dependencies, location)

        return stack, i, dependencies

    def _parse_one_word(
            self,
            expr: str,
            i: int,
            stack: list[Any],
            dependencies: Set[Location],
            location: Location
    ) -> int:
        char = expr[i]
        if char.isdigit() and not (i + 1 < len(expr) and expr[i + 1] == ":"):
            number = extract_number(expr[i:])
            stack.append([number])
            return i + len(number)
        elif char == "+" and expr[i + 1].isdigit() and (
                i == 0 or (isinstance(stack[-1], str) and isinstance(safe_float(stack[-1]), str))):
            # support implicit positive numbers
            number = extract_number(expr[i + 1:])
            stack.append([number])
            return i + len(number) + 1
        elif char == "-" and expr[i + 1].isdigit() and (
                i == 0 or (isinstance(stack[-1], str) and isinstance(safe_float(stack[-1]), str))):
            # support negative numbers
            number = extract_number(expr[i + 1:])
            stack.append([f"-{number}"])
            return i + len(number) + 1
        elif char == "(":
            sub_expr = expr[i + 1: find_closing_parentheses(expr, i + 1)]
            rest, j, new_dependencies = self.parse(sub_expr, location)
            dependencies.update(new_dependencies)
            stack.append([rest])
            return i + len(sub_expr) + 1
        elif char in [" ", "\n", ")"]:  # do nothing keys
            return i + 1
        return i + self._extract_word_token(expr[i:], stack, dependencies, location)

    def _extract_word_token(
            self,
            expr: str,
            stack: list[Any],
            dependencies: Set[Location],
            location: Location
    ) -> int:
        word, first_part, second_part, third_part = "", "", "", ""
        i = 0
        while i < len(expr):
            c = expr[i]
            word, first_part, second_part, third_part = \
                _append_to_words(c, first_part, second_part, third_part, word)

            if i + 1 < len(expr) and (word + expr[i + 1]) in self.pair_operations:
                word += expr[i + 1]
                stack.append(word)
                return len(word)
            elif word in self.pair_operations:
                stack.append(word)
                return len(word)
            if word in self.reduce_operations and (expr[i + 1] == "("):
                return i + self._extract_reduce_word_token(expr[i:], word, location, stack, dependencies)

            if is_word_a_pointer(expr, i, first_part, second_part):
                self._extract_pointer_word(first_part, second_part, third_part, location, stack, dependencies)
                return i + 1

            i += 1
        stack.append(word)  # probably just a string
        return len(word)

    def _extract_reduce_word_token(
            self,
            expr: str,
            word: str,
            location: Location,
            stack: list[Any],
            dependencies: Set[Location]
    ) -> int:
        i = 1
        sub_stack = []
        if expr[i] != "(":
            raise EvaluationError("After function ( should be")
        expr_input = expr[i + 1: find_closing_parentheses(expr, i + 1)]
        for var in split_in_upper_parentheses(expr_input, ","):
            var_stack, j, new_dependencies = self.parse(var, location)
            i += j + 1
            dependencies.update(new_dependencies)
            if var_stack[0] == "%table%":
                sub_stack.extend(var_stack[1:])
            elif all(isinstance(item, list) for item in var_stack):
                sub_stack.append(var_stack)
            else:
                sub_stack.append([var_stack])

        stack += [word, sub_stack]
        return i

    def _extract_pointer_word(
            self,
            first_part: str,
            second_part: str,
            third_part: str,
            location: Location,
            stack: list[Any],
            dependencies: Set[Location]
    ) -> None:
        sub_table = self._extract_sub_table(first_part, second_part, third_part, location, dependencies)
        if sub_table is None:
            raise EvaluationError("BadPointer")
        for row in sub_table:
            stack.append(row)

    def _extract_sub_table(
            self,
            first_part: str,
            second_part: str,
            third_part: str,
            location: Location,
            dependencies: Set[Location]
    ) -> Union[None, list[Any]]:
        sheet_name, start_word, end_word \
            = self._order_string_location(first_part, second_part, third_part, location.sheet)

        worksheet = self.workbook.get_worksheet(sheet_name, True)
        if not (len(start_word) > 1 or end_word) or not worksheet:
            return None

        start_row, start_col = extract_word_location(start_word)
        if start_row is None and start_col is None:
            return None

        end_row, end_col = extract_word_location(end_word)

        if ((start_col is not None) and (start_row is not None)) and ((end_col is None) and (end_row is None)):
            path = Location(sheet=worksheet.name, column=start_col if start_col else 0, row=start_row)
            loc = self.workbook.get_cell(path).location

            dependencies.add(loc)
            return [self.workbook.get_cell(loc).evaluation]

        end_col, end_row, start_col, start_row = \
            normalize_table_pointer(start_row, start_col, end_row, end_col, worksheet)

        return self._extract_table(sheet_name, start_row, start_col, end_row, end_col, dependencies)

    def _extract_table(
            self,
            sheet_name: str,
            start_row: int,
            start_col: int,
            end_row: int,
            end_col: int,
            dependencies: Set[Location]
    ) -> list[Any]:
        table: list[Any] = ["%table%"]
        for col_index in range(start_col, end_col + 1):
            column = []
            for row_index in range(start_row, end_row + 1):
                loc = Location(sheet=sheet_name, column=col_index, row=row_index)
                cell = self.workbook.get_cell(loc)
                dependencies.add(cell.location)
                evaluation = cell.evaluation
                column.append([evaluation if evaluation else 0])
            table.append(column)
        return table

    def _order_string_location(
            self,
            first_part: str,
            second_part: str,
            third_part: str,
            current_sheet_name: str
    ) -> Tuple[str, str, str]:

        sheet_name, start_word, end_word = "", "", ""
        if third_part:
            sheet_name = first_part
            start_word = second_part
            end_word = third_part
        elif second_part:
            if self.workbook.get_worksheet(first_part, True):
                sheet_name = first_part
                start_word = second_part
            else:
                sheet_name = current_sheet_name
                start_word = first_part
                end_word = second_part
        else:
            sheet_name = current_sheet_name
            start_word = first_part
        return sheet_name, start_word, end_word
