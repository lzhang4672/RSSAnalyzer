import csv
import os
from typing import Any


def read_file(file: str) -> list[dict[str, str]]:
    """Reads a csv file and returns it as a dictionary"""
    ret = []
    if os.path.exists(file):
        with open(file, errors='ignore') as csv_file:
            reader = csv.reader(csv_file)
            fields = next(reader)
            for row in reader:
                ret += [{fields[i]: row[i] for i in range(len(row))}]
    return ret


def write_to_file(file_name: str, fields: list[str], rows: list[dict[str, Any]]) -> None:
    """Function that writes to a csv file.

    Preconditions:
        - file_name ends in the valid .csv format
        - fields != []
        - every row in rows has proper amount of keys and the keys match with fields (luke implement)
    """
    with open(file_name, 'w', encoding='UTF8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        # write the fields
        writer.writeheader()
        # write the rows
        for row in rows:
            writer.writerow(row)


if __name__ == '__main__':
    import doctest
    import python_ta

    doctest.testmod(verbose=True)

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'os', 'typing'],
        'allowed-io': [],
        'max-nested-blocks': 10
    })
