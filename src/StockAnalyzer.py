from __future__ import annotations
from typing import Optional
from dataclasses import dataclass, field

CACHE_DIRECTORY = 'scrape_cache/'



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
    sentiment: float


@dataclass
class AnalyzeProgress:
    """A dataclass represent the progress of analyzation for a stock


    Instance Attributes:
        - stock: the stock object to be analyzed

    """
    stock: Stock
    articles_analyzed: int



class StockAnalyzer:
    """This class that analyzes information for stocks.


     Instance Attributes:
     - id: a string representing the id associated with analyzation.
     - tickers: a list of stock tickers to be analyzed by the object.
     - use_cache: a boolean representing if the object should use the cache saved with the id.
                  If a cache with the specified id exists and use_cache is True, then the object will not scrape news
                  articles and instead build itself of the cached data.
                  Otherwise, the object will scrape the internet for news articles associated with the tickers and
                  build itself based on that while saving a cache with the associated id.

    """
    def _build_data(self):

    def __init__(self, id: str, tickers: list[str], use_cache: Optional[bool] = True):
        """Initalize a StockAnalyzer object with the given tickers to analyze.

        Preconditions:
        - len(tickers) > 0
        - all ticker in tickers exist inside the data/tickers_data.csv file
        """
        self._id = id
        self.tickers = tickers
        self.use_cache = use_cache

        if not use_cache:
            self._build_data()

