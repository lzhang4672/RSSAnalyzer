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
    tickers: dict[str, Ticker]
    def __init__(self, csv: str):
        with open(csv) as f:
            reader =
