import os
import pickle
from typing import Iterable, NoReturn

import const.const as const
from core.coder import Coder
from core.decoder import Decoder
from core.table import Table
import collections as c

from misc.singleton import Singleton


class FSOperator(metaclass=Singleton):
    def create_table_from_file(self, filename: str, encoding: str) -> Table:
        counter = c.Counter()
        with open(filename, encoding=encoding, mode='r') as file:
            for line in file:
                for char in line:
                    counter[char] += 1
        return Table(dict(counter))

    def read_chars_from_file(self, filename: str,
                             encoding: str) -> Iterable[str]:
        with open(filename, encoding=encoding, mode='r') as file:
            for line in file:
                for char in line:
                    yield char

    def write_table_to_file(self, filename: str, table: Table) -> NoReturn:
        with open(filename, encoding='utf-8', mode='a') as file:
            file.write(const.MARK_TABLE_START + '\n')
            file.write(str(pickle.dumps(table)))
            file.write('\n')
            file.write(const.MARK_TABLE_END + '\n')

    def write_coded_text_to_file(self, filename: str, encoding: str,
                                 coded_chars: Iterable[str]) -> NoReturn:
        with open(filename, encoding=encoding, mode='a') as file:
            file.write(const.MARK_TEXT_START + '\n')
            for char in coded_chars:
                file.write(char)
            file.write('\n')
            file.write(const.MARK_TEXT_END + '\n')

    def code_file(self, input_filename: str,
                  output_filename: str, encoding: str) -> NoReturn:
        self.create_new_output_file(output_filename)
        table = self.create_table_from_file(input_filename, encoding)
        chars_iterator = self.read_chars_from_file(input_filename, encoding)
        coder = Coder(table)
        self.write_table_to_file(output_filename, table)
        coded_chars_iterator = coder.code_chars_lazy(chars_iterator)
        self.write_coded_text_to_file(output_filename, encoding,
                                      coded_chars_iterator)

    def read_table_from_coded_file(self, filename: str,
                                   encoding: str) -> Table:
        with open(filename, encoding=encoding, mode='r') as file:
            next_table = False
            for line in file:
                if next_table:
                    return pickle.loads(eval(bytearray(line, encoding)))
                if line.startswith(const.MARK_TABLE_START):
                    next_table = True

    def read_coded_bits_from_coded_file(self, filename: str,
                                        encoding: str) -> Iterable[str]:
        with open(filename, encoding=encoding, mode='r') as file:
            next_table = False
            for line in file:
                if next_table:
                    for bit in line:
                        yield bit
                    raise StopIteration()
                if line.startswith(const.MARK_TEXT_START):
                    next_table = True
        raise StopIteration()

    def decode_file(self, input_filename: str,
                    output_filename: str, encoding: str) -> NoReturn:
        self.create_new_output_file(output_filename)
        table = self.read_table_from_coded_file(input_filename, encoding)
        bits_iterator = self.read_coded_bits_from_coded_file(input_filename,
                                                             encoding)
        decoder = Decoder(table)
        coded_chars_iterator = decoder.decode_lazy_from_bits(bits_iterator)
        with open(output_filename, encoding=encoding, mode='a') as file:
            for char in coded_chars_iterator:
                file.write(char)

    def create_new_output_file(self, filename: str) -> NoReturn:
        if os.path.exists(filename):
            raise IOError('file exist')
        if not os.path.exists(filename):
            with open(filename, 'a'):
                pass
