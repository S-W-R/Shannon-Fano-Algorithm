import math
from typing import Counter, Dict, List, Tuple, Union


class Table:
    def __init__(self, char_table: Dict[str, Union[int, float]]):
        self._char_to_code_table = self.__create_code_table(char_table)
        self._code_to_char_table = {code: char for char, code in
                                    self._char_to_code_table.items()}

    def __create_code_table(self, char_table: Dict[str, Union[int, float]],
                            current_code='', code_table=None):
        if code_table is None:
            code_table = dict()
        if len(char_table) > 1:
            left, right = self.__divide_table(char_table)
            self.__create_code_table(left, current_code + '0', code_table)
            self.__create_code_table(right, current_code + '1', code_table)
        elif len(char_table) == 1:
            code_table[next(iter(char_table.keys()))] = current_code
        return code_table

    def __divide_table(self, char_table: Dict[str, Union[int, float]]):
        table = sorted(char_table.items(), key=lambda x: x[1], reverse=True)
        # type: List[Tuple[str, int]]
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

    def __str__(self):
        return self._char_to_code_table.__str__()
