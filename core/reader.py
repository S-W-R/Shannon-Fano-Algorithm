from core.table import Table
import collections as c


def create_table_from_file(filename: str) -> Table:
    counter = c.Counter()
    with open(filename, encoding='utf-8', mode='r') as file:
        for line in file:
            for char in line:
                counter[char] += 1
    return Table(dict(counter))
