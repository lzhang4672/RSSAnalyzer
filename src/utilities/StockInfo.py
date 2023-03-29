from python_ta.contracts import check_contracts
import csv
from CSV import read_file
from typing import Optional

tickers = read_file('../data/tickers_data.csv')


def get_info_from_ticker(ticker: str, csv_dict: list[dict]) -> Optional[dict]:
    """
    Returns the dictionary inside the given list that corresponds to the ticker
    If the symbol is not found, returns None
    """
    for stock in csv_dict:
        if ticker in stock:
            return stock

    return None
