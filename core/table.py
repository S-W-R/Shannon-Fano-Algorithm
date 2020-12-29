import math
from typing import Dict, List, Tuple, Union

from const import const


class Table:
    ESCAPE_SYMBOL = None

    def __init__(self, char_table: Dict[str, int]):
        char_table[self.ESCAPE_SYMBOL] = 0
        self._char_to_code_table = self.__create_code_table(char_table)
        char_codes = self._char_to_code_table
        self._escape_symbol_code = self.__create_escape_symbol_code(char_table,
                                                                    char_codes)
        self._char_to_code_table.pop(Table.ESCAPE_SYMBOL)
        self._max_code_length = len(max(self._char_to_code_table.values(),
                                        key=len))
        self._max_code_length = max(self._max_code_length,
                                    len(self._escape_symbol_code))
        self._code_to_char_table = {code: char for char, code in
                                    self._char_to_code_table.items()}

    @staticmethod
    def __create_escape_symbol_code(char_table: Dict[str, int],
                                    char_to_code_table: Dict[str, str]) -> str:
        remainder = 0
        escape_symbol_code = char_to_code_table[Table.ESCAPE_SYMBOL]
        for char, count in char_table.items():
            code_length = len(char_to_code_table[char]) * count
            remainder = (remainder + code_length) % const.BYTE_LENGTH
        return escape_symbol_code + ('1' * remainder)

    @staticmethod
    def __create_code_table(char_table: Dict[str, Union[int, float]],
                            current_code='', code_table=None):
        if code_table is None:
            code_table = dict()
        if len(char_table) > 1:
            left, right = Table.__divide_table(char_table)
            Table.__create_code_table(right, current_code + '0', code_table)
            Table.__create_code_table(left, current_code + '1', code_table)
        elif len(char_table) == 1:
            code_table[next(iter(char_table.keys()))] = current_code
        return code_table

    @staticmethod
    def __divide_table(char_table: Dict[str, Union[int, float]]):
        table = sorted(char_table.items(), key=lambda x: x[1], reverse=True)
        # type: List[Tuple[str, Union[int, float]]]
        # bug incorrect return typing except List[str], really List[Tuple[]]
        left_weight = sum(item[1] for item in table)
        right_weight = 0
        optimal_difference = math.inf
        index = 0
        for i in range(len(table)):
            index = i
            new_weight = table[i][1]
            left_weight -= new_weight
            right_weight += new_weight
            new_difference = abs(left_weight - right_weight)
            if new_difference >= optimal_difference:
                break
            optimal_difference = new_difference

        return dict(table[:index]), dict(table[index:])

    def get_char_code(self, char: str):
        return self._char_to_code_table[char]

    def get_char_by_code(self, code: str):
        return self._code_to_char_table[code]

    def contain_code(self, code: str):
        return code in self._code_to_char_table

    @property
    def max_code_length(self) -> int:
        return self._max_code_length

    @property
    def escape_symbol_code(self) -> str:
        return self._escape_symbol_code

    def __str__(self):
        return self._char_to_code_table.__str__()
