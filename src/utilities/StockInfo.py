@check_contracts
class Ticker:
    """A Ticker represents a stock in a network.
    Instance Attributes:
    - symbol: the symbol of the stock
    - name: the full name of the company
    - industry: the category the company belongs to
    - market_cap: the current netvalue of the company """
    symbol: str
    name: str
    industry: str
    market_cap: int
    def __init__(self, symbol: str, name: str, industry: str, market_cap: int):
        self.symbol = symbol
        self.name = name
        self.industry = industry
        self.market_cap = market_cap

@check_contracts
class StockInfo:
    """A mapping of all ticker names in the network, to their repsective Ticker attributes.
    Instance Attributes:
    - _tickers: a dictionary with ticker symbols as keys and corresponding Ticker as values """
    _tickers: dict[str, Ticker]
    def __init__(self, csv: str):
        self._tickers = csv_reader(csv)
    def get_ticker_name(self, symbol: str):
        return self._tickers[symbol].name
    def get_ticker_industry(self, symbol: str):
        return self._tickers[symbol].industry
    def get_ticker_market_cap(self, symbol: str):
        return self._tickers[symbol].market_cap

def csv_reader(csv: str) -> dict[str, Ticker]:
    """Return a mapping of ticker symbols to the Ticker object"""
    with open(csv) as f:
        next(f)
        reader = {ticker[0]: Ticker(ticker[0], ticker[1], ticker[2], int(ticker[3])) for ticker in f}
        return reader
