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
import CSV
import StockInfo
from StockInfo import get_tickers
from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings
from StockGraphAnalyzer import StockGraphAnalyzer
from GraphVisualizer import GraphVisualizer
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
    StockInfo.tickers = CSV.read_file('data/tickers_data.csv')
    tickers = get_tickers()
    analyzer = StockAnalyzer(tickers, default_settings)
    stock_graph_analyzer = StockGraphAnalyzer(analyzer)
    stock_graph_analyzer.generate_graph()
    graph_visualizer = GraphVisualizer(default_settings.id, stock_graph_analyzer.graph)
    graph_visualizer.show_graph()


if __name__ == '__main__':
    run_analysis()
