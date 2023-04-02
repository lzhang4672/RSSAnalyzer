"""
This Python Module contains a function to run StockAnalyzer.py

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and professors
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mark Zhang, Li Zhang and Luke Zhang
"""
import StockAnalyzer
from StockInfo import get_tickers
from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# CONSTANTS
default_settings = StockAnalyzerSettings(id='all_tickers_10_articles', articles_per_ticker=10, use_cache=True,
                                         search_focus='Stock')


def run_analysis() -> None:
    """
    A top level function for this module to scrape articles for the tickers inside the csv

    Preconditions:
        - default settings is valid
    """
    tickers = get_tickers()
    analyzer = StockAnalyzer(tickers, default_settings)
    print("done")


if __name__ == '__main__':
    run_analysis()
