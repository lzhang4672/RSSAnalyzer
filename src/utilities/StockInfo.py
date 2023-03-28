def csv_reader(csv: str):
    with open(csv) as f:
        next(f)
        reader = {ticker[0]: Ticker(ticker[0], ticker[1], ticker[2], int(ticker[3])) for ticker in f}
        return reader
class Ticker:
    symbol: str
    name: str
    industry: str
    market_cap: int
    def __init__(self, symbol: str, name: str, industry: str, market_cap: int):
        self.symbol = symbol
        self.name = name
        self.industry = industry
        self.market_cap = market_cap


class StockInfo:
    _tickers: dict[str, Ticker]
    def __init__(self, csv: str):
        self._tickers = csv_reader(csv)
    def get_ticker_name(self, symbol: str):
        return self._tickers[symbol].name
    def get_ticker_industry(self, symbol: str):
        return self._tickers[symbol].industry
    def get_ticker_market_cap(self, symbol: str):
        return self._tickers[symbol].market_cap
