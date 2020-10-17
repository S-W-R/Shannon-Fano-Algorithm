from typing import Counter, Dict, List, Tuple, Union


class Table:
    def __init__(self, char_table: Dict[str, Union[int, float]]):
        self._code_table = self.__create_code_table(char_table)
        self._char_table = {code: char for char, code in
                            self._code_table.items()}

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
        left_table = sorted(char_table.items(), key=lambda x: x[1])
        # type: List[Tuple[str, int]]
        # bug incorrect return typing except List[str], really List[Tuple[]]
        right_table = []
        left_weight = sum(item[1] for item in left_table)
        right_weight = 0
        while left_weight > right_weight:
            right_item = left_table.pop()
            left_weight -= right_item[1]
            right_weight += right_item[1]
            right_table.append(right_item)
        return dict(left_table), dict(right_table)

    def get_char_code(self, char: str):
        return self._code_table[char]

    def get_char_by_code(self, code: str):
        return self._char_table[code]
