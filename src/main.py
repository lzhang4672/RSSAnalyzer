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
from python_ta.contracts import check_contracts
import CSV
import StockInfo
import GUI
import ssl
import nltk
from StockInfo import get_tickers
from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings
from StockGraphAnalyzer import StockGraphAnalyzer
from GraphVisualizer import GraphVisualizer
import os

if __name__ == '__main__':
    # set relative path
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # set up StockInfo's data
    StockInfo.tickers = CSV.read_file('data/tickers_data.csv')
    # download nltk data
    # avoid the download popup with ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    # install vader_lexicon model
    nltk.downloader.download('stopwords')
    nltk.downloader.download('vader_lexicon')
    # load in GUI
    main_screen = GUI.MainMenu()
    # run_analysis()
