import os
os.chdir(os.path.dirname(os.path.abspath(file)))
import StockAnalyzer
from StockInfo import get_tickers
from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings



# CONSTANTS
default_settings = StockAnalyzerSettings(id='all_tickers', articles_per_ticker=20, use_cache=True,
                                         search_focus='Competitors')

def run_analysis() -> None:

    tickers = get_tickers()
    analyzer = StockAnalyzer(tickers, default_settings)


if name == 'main':
    run_analysis()
