from __future__ import annotations
from typing import Optional
from dataclasses import dataclass, field
from CSV import read_file
from StockInfo import get_info_from_ticker
from NewsScraper import NewsArticleContent, NewsScraper, PUBLISH_RANGE
import json
import os

CACHE_DIRECTORY = 'scrape_cache/'
CACHE_HEADERS = [
    'Symbol', 'PrimaryArticlesAnalyzed', ''
]



# EXCEPTIONS

class StockAnalyzeError(Exception):
    """A base class exception for the class"""


class CacheDoesNotExistError(StockAnalyzeError):
    """Thrown when a cached data wants to be used but the cached data associated with the id does not exist"""


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
    sentiment: float = 0


@dataclass
class StockAnalyzeData:
    """A dataclass represent the progress of analyzation for a stock


    Instance Attributes:
        - stock: the primary stock to be analyzed
        - primary_articles_data: a list representing the articles analyzed that are specifically focusing on the stock
                                in a tuple format where the first element is the url of the article and the
                                second element is the sentiment value calculated form the article.
        - linking_articles_data: a list representing outside articles that mention the stock in a tuple format where
                                the first element is the url of the article and the second element is the sentiment
                                value calculated from the article.
        - connected_stocks: a dictionary with the key as a stock and an integer representing the frequency of that
                            specific stock being mentioned in articles that focus specifically on the primary stock.
    """
    stock: Stock
    scraper: NewsScraper
    primary_articles_data: list[tuple[str, float]] = field(default_factory=list)
    linking_articles_data: list[tuple[str, float]] = field(default_factory=list)
    connected_stocks: dict[Stock, int] = field(default_factory=list)

@dataclass
class StockAnalyzerSettings:
    """a dataclass representing the settings to be used when StockAnalyzer does its analyzing.

    Instance Attributes:
        - articles_per_ticket: the number of articles that will be analyzed per ticker.
        - use_cache: a boolean representing if the object should use the cache saved with the id.
                  If a cache with the specified id exists and use_cache is True, then the object will not scrape news
                  articles and instead build itself of the cached data.
                  Otherwise, the object will scrape the internet for news articles associated with the tickers and
                  build itself based on that while saving a cache with the associated id.
        - id: a string representing the id associated with analyzation.
        - cache_root: a string representing the folder location of where the cached analyzed data should be stored.
        - output_info: a boolean representing if information should be printed to the console on the analyzation process

    Representation Invariants:
        - self.articles_per_ticker > 0
        - any(PUBLISH_RANGE[key] == self.articles_publish_range for key in PUBLISH_RANGE)
    """

    id: str
    articles_per_ticker: int = 15
    use_cache: bool = False
    cache_root: str = CACHE_DIRECTORY
    output_info: bool = True
    articles_publish_range: str = PUBLISH_RANGE['Recent']


class StockAnalyzer:
    """This class that analyzes information for stocks.


     Instance Attributes:
        - tickers: a list of stock tickers to be analyzed by the object.
     Private Instance Attributes:
        - _settings: a StockAnalyzerSettings object that represents the settings to be used when analyzing the stocks.
        - _data: a dictionary containing all the data of the stocks analyzed
    """

    tickers: list[str]
    _settings: StockAnalyzerSettings
    _analyze_data: dict[str, AnalyzeData] = {}




    def _save_cache(self):
        """Called to save the current progress of scraping to a csv file.
        """
        






    def _analyze_stock(self, ticker):
        stock_analyze_data = self._analyze_data[ticker]
        stock_analyze_data.scraper.scrape_articles()
        for url in stock_analyze_data.scraper.articles_scraped:
            print(url)


    def _build_data(self):
        """This private function is responsible for scraping news articles and building up data for the
        sentiment values associated with a stock """
        if self._settings.output_info:
            print("Starting Analyzation...")
        if self._settings.use_cache:
            if self._settings.output_info:
                print("Loading Scrape Data From Cache")
            # load cached data if it exists
            cached_data = read_file(CACHE_DIRECTORY + self._settings.id + '.csv')
            # load the cached data into local variables
            for row in cached_data:
                # get all row data
                ticker = row['Symbol']

                stock_analyze_data = self._analyze_data[ticker]
                if stock_analyze_data:
                    # the stock analyze data exists for the ticker
                    if self._settings.output_info:
                        print("Loading Cached Data For: " + ticker)
                    primary_articles_analyzed = json.loads(row['PrimaryArticlesAnalyzed'])
                    primary_articles_sentiment_scores = json.loads(row['ArticlesSentimentScores'])
                    connected_companies = json.loads(row['ConnectedCompanies'])
                    connected_frequencies = json.loads(row['ConnectedFrequency'])
                    linking_articles_analyzed = json.loads(row['LinkingArticlesAnalyzed'])
                    linking_articles_sentiment_scores = json.loads(row['LinkingArticlesSentimentScores'])
                    # load in primary articles data
                    for i in range(len(primary_articles_analyzed)):
                        article_link = primary_articles_analyzed[i]
                        article_sentiment = primary_articles_sentiment_scores[i]
                        stock_analyze_data.primary_articles_data += (article_link, article_sentiment)
                    # load in linking articles data
                    for i in range(len(linking_articles_analyzed)):
                        article_link = linking_articles_analyzed[i]
                        article_sentiment = linking_articles_sentiment_scores[i]
                        stock_analyze_data.linking_articles_data += (article_link, article_sentiment)
                    # load in connected stocks
                    for i in range(len(connected_companies)):
                        ticker, frequency = connected_companies[i], connected_frequencies[i]
                        stock_analyze_data.connected_stocks[ticker] = frequency
        # scrape for data if required
        if self._settings.output_info:
            print("Starting Web Scrape")
        for ticker in self._analyze_data:
            self._analyze_stock(ticker)


        if self._settings.output_info:
            print("Done Web Scrape")

    def __init__(self, tickers: list[str],
                 settings: StockAnalyzerSettings = StockAnalyzerSettings(id="Default", articles_per_ticker=15,
                                                                         use_cache=True)):
        """Initalize a StockAnalyzer object with the given tickers to analyze.

        Preconditions:
        - len(tickers) > 0
        - all ticker in tickers exist inside the data/tickers_data.csv file
        """
        self.tickers = tickers
        self._settings = settings

        if self._settings.output_info:
            print("Fetching Stocks...")
        # set up the stocks and initalize the progress
        for ticker in self.tickers:
            stock_info = get_info_from_ticker(ticker)
            if stock_info is not None:
                if self._settings.output_info:
                    print('Found Data For: ' + ticker)
                self._analyze_data[ticker] = StockAnalyzeData(
                    Stock(
                        name=stock_info['Name'],
                        ticker=stock_info['Symbol'],
                        market_cap=float(stock_info['Market Cap']),
                        industry=stock_info['Industry'],
                        sentiment=0,
                    ),
                    scraper=NewsScraper(
                        search_query=stock_info['Name'] + ' stock competitors news',
                        number_of_articles=self._settings.articles_per_ticker,
                        publish_range=self._settings.articles_publish_range
                    )
                )
            else:
                if self._settings.output_info:
                    print(ticker + ' was not found in the database')

        self._build_data()
