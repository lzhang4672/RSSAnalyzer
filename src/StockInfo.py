from python_ta.contracts import check_contracts
import csv
from CSV import read_file
from typing import Optional

tickers = read_file('data/tickers_data.csv')


def get_info_from_ticker(ticker: str) -> dict[str, str] | None:
    """
    Returns the dictionary inside the given list that corresponds to the ticker
    If the symbol is not found, returns None
    """

    for stock in tickers:
        if ticker.upper() == stock['Symbol'].upper():
            return stock

    return None


def get_ticker_from_name(name: str) -> str | None:
    """
    Returns the corresponding dictionary to the name specified
    Otherwise returns None if not found
    """
    for stock in tickers:
        if name.upper() == stock['Name'].upper():
            return stock['Symbol'].upper()
    return None


def get_tickers() -> list[str]:
    """
    Returns a list containing all the tickers in the csv
    """
    return [stock['Symbol'] for stock in tickers]


def get_tickers_and_names() -> tuple[set, set]:
    """
    Returns tickers and names in the tickers list
    """
    symbols, names = set(), set()
    for element in tickers:
        symbols.add(element['Symbol'])
        names.add(element['Name'].upper())
    return symbols, names
