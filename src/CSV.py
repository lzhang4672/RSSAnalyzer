import csv
import os


def read_file(file: str) -> list[dict[str, str]]:
    """Reads a csv file and returns it as a dictionary"""
    ret = []
    if os.path.exists(file):
        # check if path exists first
        with open(file) as csv_file:
            reader = csv.reader(csv_file)
            fields = next(reader)
            for row in reader:
                ret += [{fields[i]: row[i] for i in range(len(row))}]
    return ret

def csv_updater(file: str, new_ticker: dict):
    """Adds new ticker to the end of the csv file.
    Instance Atttributes:
    - new_ticker: dictionary with keys as the attribute of the ticker, and the corresponding values are
    values of the ticker attribute. must be in the order: symbol, name,  industry, market cap"""
    with open(file, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writerow(new_ticker)
        csv_file.close()

