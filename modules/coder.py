from typing import Iterable

from modules.table import Table


class Coder:
    def __init__(self, code_table: Table):
        self._code_table = code_table

    def code_text(self, text: str) -> str:
        coded_text = ''
        for char in text:
            coded_text += self._code_table.get_char_code(coded_text)
        return coded_text

    def code_chars(self, chars: Iterable[str]) -> Iterable[str]:
        for char in chars:
            yield self._code_table.get_char_code(char)

    def code_lines(self, lines: Iterable[str]) -> Iterable[str]:
        for line in lines:
            yield self.code_text(line)
