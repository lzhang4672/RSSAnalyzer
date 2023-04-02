import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import StockAnalyzer
from StockInfo import get_tickers
from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings



# CONSTANTS
default_settings = StockAnalyzerSettings(id='all_tickers_competitors_focus', articles_per_ticker=10, use_cache=True,
                                         search_focus='Competitors')

def run_analysis() -> None:

    tickers = get_tickers()
    analyzer = StockAnalyzer(tickers, default_settings)
    print("done")


if __name__ == '__main__':
    run_analysis()
