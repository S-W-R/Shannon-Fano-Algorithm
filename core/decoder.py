from typing import Iterable
from core.table import Table


class Decoder:
    def __init__(self, code_table: Table):
        self._code_table = code_table

    def decode_lazy_from_bits(self, bits: Iterable[str]) -> Iterable[str]:
        bit_sequence = ''
        for bit in bits:
            bit_sequence += str(bit)
            if len(bit_sequence) > self._code_table.max_code_length:
                raise Exception(f'cannot decode: {bit_sequence} not in table')
            elif bit_sequence == self._code_table.escape_symbol_code:
                return
                # raise StopIteration()
            elif self._code_table.contain_code(bit_sequence):
                yield self._code_table.get_char_by_code(bit_sequence)
                bit_sequence = ''
