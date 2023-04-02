"""
This Python module contains the classes
"""
from python_ta.contracts import check_contracts
from dataclasses import dataclass, field
import csv
from CSV import read_file
from typing import Optional

tickers = read_file('data/tickers_data.csv')


@dataclass
class Stock:
    """A dataclass to store a stock's data.

    Instance Attributes:
        - name: The company name associated with the stock.
        - ticker: The company's ticker.
        - market_cap: The company's market cap (in billions)
        - industry: The industry the company is in
        - sentiment: The sentiment value associated with the stock

    Representation Invariants:
        - self.name != ''
        - self.ticker != ''
        - 0 < self.market_cap
        - self.industry != ''
        - -10 <= self.sentiment <= 10
    """
    name: str
    ticker: str
    market_cap: float
    industry: str
    sentiment: float = 0


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
