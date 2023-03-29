import csv

field_names = ['symbol', 'name', 'industry', 'market cap']
def csv_reader(file: str) -> dict[str, dict[str, str]]:
    """Return a mapping of ticker symbols to the Ticker object"""
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        d = {line[0]: {'name': line[1], 'industry': line[2], 'market cap': line[3]}
             for line in reader}
    return d

def csv_updater(file: str, new_ticker: dict):
    """Adds new ticker to the end of the csv file.
    Instance Atttributes:
    - new_ticker: dictionary with keys as the attribute of the ticker, and the corresponding values are
    values of the ticker attribute. must be in the order: symbol, name,  industry, market cap"""
    with open(file, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writerow(new_ticker)
        csv_file.close()


