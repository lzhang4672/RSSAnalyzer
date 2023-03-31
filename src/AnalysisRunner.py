from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings
from StockInfo import get_tickers



# CONSTANTS
default_settings = StockAnalyzerSettings(id='all_tickers', articles_per_ticker=10, use_cache=True)


def run_analysis() -> None:
    tickers = get_tickers()
    analyzer = StockAnalyzer(tickers, default_settings)


if __name___ == "__main__":
    run_analysis()
