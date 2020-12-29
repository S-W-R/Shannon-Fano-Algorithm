from typing import Iterable
from core.table import Table


class Coder:
    def __init__(self, code_table: Table):
        self._code_table = code_table

    def code_chars_lazy(self, chars: Iterable[str]) -> Iterable[str]:
        for char in chars:
            yield self._code_table.get_char_code(char)
        yield self._code_table.escape_symbol_code
