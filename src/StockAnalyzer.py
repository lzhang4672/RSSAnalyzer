"""
This Python module contains all the nessecary functions and classes for running the functions to get the scraped data
from NewsScraper.py and then processing the data by running/calling the nessecary classes and functions inside
Sentiment.py
"""
from __future__ import annotations
from python_ta.contracts import check_contracts
from typing import Optional
from dataclasses import dataclass, field
from CSV import read_file, write_to_file
from StockInfo import get_info_from_ticker
from NewsScraper import NewsArticleContent, NewsScraper, PUBLISH_RANGE, get_content_from_article_url
from Sentiment import get_sentiment_for_article
from StockInfo import Stock
from LiveDisplay import Window
import time
import ast
import random
import os

CACHE_DIRECTORY = 'scrape_cache/'
CACHE_HEADERS = [
    'Ticker', 'ArticlesUrls', 'ArticlesSentimentScores', 'ConnectedTickers', 'ConnectedFrequency',
    'LinkingArticlesUrls', 'LinkingArticlesSentimentScores', 'DoneScraping'
]
SEARCH_FOCUS = {
    'Competitors': ' stock competitors news',
    'Stock': ' stock news',
    'General': ' news',
}




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
        - connected_tickers: a dictionary with the key as a stock's ticker and an integer representing the frequency of
                     .       that specific stock being mentioned in articles that focus specifically on the primary stock
    """
    stock: Stock
    scraper: NewsScraper
    primary_articles_data: list[tuple[str, float]] = field(default_factory=list)
    linking_articles_data: list[tuple[str, float]] = field(default_factory=list)
    connected_tickers: dict[str, int] = field(default_factory=dict)
    done_scraping: bool = False

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
        - id: a string representing the cached csv file name associated with analyzation.
        - cache_root: a string representing the folder location of where the cached analyzed data should be stored.
        - output_info: a boolean representing if information should be printed to the console on the analyzation process

    Representation Invariants:
        - self.articles_per_ticker > 0
        - any(key == self.articles_publish_range for key in PUBLISH_RANGE)
        - any(key == self.search_focus for key in SEARCH_FOCUS)
    """

    id: str
    articles_per_ticker: int = 5
    use_cache: bool = False
    cache_root: str = CACHE_DIRECTORY
    output_info: bool = True
    articles_publish_range: str = 'Recent'
    search_focus: str = 'Stock'



# helper methods
#@check_contracts
def _get_median_sentiment_score(articles_data: list[tuple[str, float]]) -> float:
    # filter out all the sentiment values that are exactly. Usually, if the sentiment is exactly 0 then we shouldn't
    # count it as the sentiment is too neutral.
    sorted_articles_data = [data for data in articles_data if data[0] != 0]
    # don't mutate and sort by the tuple's float value
    sorted_articles_data.sort(key=lambda tup: tup[1])
    len_articles = len(articles_data)
    mid_index = (len_articles - 1) // 2
    if len_articles % 2 == 0:
        # length is even
        return (sorted_articles_data[mid_index][1] + sorted_articles_data[mid_index + 1][1]) / 2.0
    else:
        return float(sorted_articles_data[mid_index][1])

class StockAnalyzer:
    """This class that analyzes information for stocks.


     Instance Attributes:
        - tickers: a list of stock tickers to be analyzed by the object.
     Private Instance Attributes:
        - _settings: a StockAnalyzerSettings object that represents the settings to be used when analyzing the stocks.
        - analyze_data: a dictionary containing all the data of the stocks analyzed
    """

    tickers: list[str]
    _settings: StockAnalyzerSettings
    analyzed_data: dict[str, StockAnalyzeData] = {}
    window: Window

    #@check_contracts
    def _save_cache(self) -> None:
        """Called to save the current progress of scraping to a csv file.
        """
        if self._settings.output_info:
            print("Saving To Cache")
        row_data = []
        for ticker in self.analyzed_data:
            analyze_data: StockAnalyzeData = self.analyzed_data[ticker]
            # parse primary articles data
            primary_articles_urls = []
            primary_articles_sentiment_scores = []
            for primary_data in analyze_data.primary_articles_data:
                url = primary_data[0]
                score = primary_data[1]
                primary_articles_urls += [url]
                primary_articles_sentiment_scores += [score]
            # parse linking articles data
            linking_articles_urls = []
            linking_articles_sentiment_scores = []
            for linking_data in analyze_data.linking_articles_data:
                url = linking_data[0]
                score = linking_data[1]
                linking_articles_urls += [url]
                linking_articles_sentiment_scores += [score]
            # parse connected tickers
            connected_tickers = []
            connected_frequencies = []

            for ticker_name in analyze_data.connected_tickers:
                frequency = analyze_data.connected_tickers[ticker_name]
                connected_tickers += [ticker_name]
                connected_frequencies += [frequency]
            # add the data to rows
            row_data += [{
                'Ticker': ticker,
                'ArticlesUrls': str(primary_articles_urls),
                'ArticlesSentimentScores': str(primary_articles_sentiment_scores),
                'ConnectedTickers': str(connected_tickers),
                'ConnectedFrequency': str(connected_frequencies),
                'LinkingArticlesUrls': str(linking_articles_urls),
                'LinkingArticlesSentimentScores': str(linking_articles_sentiment_scores),
                'DoneScraping': str(analyze_data.done_scraping)
            }]
        write_to_file(CACHE_DIRECTORY + self._settings.id, CACHE_HEADERS, row_data)

    #@check_contracts
    def remove_linking_article_by_url(self, ticker: str, url: str) -> None:
        if ticker in self.analyzed_data:
            stock_analyze_data = self.analyzed_data[ticker]
            for i in range(len(stock_analyze_data.linking_articles_data)):
                linking_data = stock_analyze_data.linking_articles_data[i]
                if linking_data[0] == url:
                    stock_analyze_data.linking_articles_data.pop(i)
                    break
    #@check_contracts
    def has_analyzed_primary_article_url(self, ticker: str, url: str) -> bool:
        if ticker in self.analyzed_data:
            stock_analyze_data = self.analyzed_data[ticker]
            for primary_data in stock_analyze_data.primary_articles_data:
                if primary_data[0] == url:
                    return True

        return False
    #@check_contracts
    def has_analyzed_linking_article_url(self, ticker: str, url: str) -> bool:
        if ticker in self.analyzed_data:
            stock_analyze_data = self.analyzed_data[ticker]
            for linking_data in stock_analyze_data.linking_articles_data:
                if linking_data[0] == url:
                    return True

        return False

    #@check_contracts
    def _analyze_stock(self, ticker: str) -> None:
        stock_analyze_data = self.analyzed_data[ticker]
        has_analyzed = False
        if len(stock_analyze_data.primary_articles_data) < self._settings.articles_per_ticker and \
                not stock_analyze_data.done_scraping and stock_analyze_data.scraper.scrape_articles():
            if self._settings.output_info:
                print("Start Analyzing " + ticker)
            for url in stock_analyze_data.scraper.articles_scraped:
                if len(stock_analyze_data.primary_articles_data) >= self._settings.articles_per_ticker:
                    break
                # sleep for a bit to not get rate limited
                time.sleep(random.uniform(0.1, 0.25))
                has_analyzed = True
                if not self.has_analyzed_primary_article_url(ticker, url):
                    print(url)
                    news_article_content = get_content_from_article_url(url)
                    if news_article_content:
                        if self._settings.output_info:
                            print("[" + ticker + "] scraping: " + url)
                        article_sentiment_data = get_sentiment_for_article(stock_analyze_data.stock,
                                                                           news_article_content)
                        if self._settings.output_info:
                            print(article_sentiment_data)
                        # update analyze data
                        stock_analyze_data.primary_articles_data += [(url, article_sentiment_data.main_sentiment_score)]
                        # update connected tickers through the linked company sentiment scores
                        for connected_ticker in article_sentiment_data.other_sentiment_scores:
                            # the ticker is not in the analyze data's connected tickers
                            if connected_ticker not in stock_analyze_data.connected_tickers:
                                stock_analyze_data.connected_tickers[connected_ticker] = 0
                            stock_analyze_data.connected_tickers[connected_ticker] += 1
                            # update linked tickers that were mentioned in the article
                            if connected_ticker in self.analyzed_data:
                                # if the connected ticker is being analyzed
                                connected_stock_analyze_data = self.analyzed_data[connected_ticker]
                                if not self.has_analyzed_linking_article_url(connected_ticker, url):
                                    # the article hasn't been linked yet so link it
                                    connected_stock_sentiment_score = \
                                        article_sentiment_data.other_sentiment_scores[connected_ticker]
                                    connected_stock_analyze_data.linking_articles_data += \
                                        [(url, connected_stock_sentiment_score)]

            # remove edge connected companies
            # get total frequencies
            total_connected_frequencies = 0
            for connected_ticker in stock_analyze_data.connected_tickers:
                total_connected_frequencies += stock_analyze_data.connected_tickers[connected_ticker]
            # compare connection frequency to see if it's frequent enough
            for connected_ticker in stock_analyze_data.connected_tickers:
                connected_frequency = stock_analyze_data.connected_tickers[connected_ticker]
                if total_connected_frequencies != 0 and connected_frequency / total_connected_frequencies <= 0.1:
                    if self._settings.output_info:
                        print("removing " + connected_ticker)
                    # connected stock's weighting is too low so just set it as 0
                    stock_analyze_data.connected_tickers[connected_ticker] = 0
                    for primary_article in stock_analyze_data.primary_articles_data:
                        # remove the associated article
                        self.remove_linking_article_by_url(connected_ticker, primary_article[0])
            if self._settings.output_info:
                print("Finished Analyzing " + ticker)
                print(stock_analyze_data)
            stock_analyze_data.done_scraping = True
            if has_analyzed:
                # if we analyzed articles and didn't rely entire only cached data
                self._save_cache()
    #@check_contracts
    def _build_data(self) -> None:
        """This private function is responsible for scraping news articles and building up data for the
        sentiment values associated with a stock """
        if self._settings.output_info:
            print("Starting Analyzation...")
        if self._settings.use_cache:
            if self._settings.output_info:
                print("Loading Scrape Data From Cache")
            # load cached data if it exists
            cached_data = read_file(CACHE_DIRECTORY + self._settings.id)
            # load the cached data into local variables
            for row in cached_data:
                # get all row data
                if row != {}:
                    ticker = row['Ticker']
                    if ticker in self.analyzed_data:
                        stock_analyze_data = self.analyzed_data[ticker]
                        if stock_analyze_data:
                            # the stock analyze data exists for the ticker
                            if self._settings.output_info:
                                print("Loading Cached Data For: " + ticker)
                            print(row['ArticlesUrls'])

                            primary_articles_analyzed = ast.literal_eval(row['ArticlesUrls'])
                            primary_articles_sentiment_scores = ast.literal_eval(row['ArticlesSentimentScores'])
                            connected_companies = ast.literal_eval(row['ConnectedTickers'])
                            connected_frequencies = ast.literal_eval(row['ConnectedFrequency'])
                            linking_articles_analyzed = ast.literal_eval(row['LinkingArticlesUrls'])
                            linking_articles_sentiment_scores = ast.literal_eval(row['LinkingArticlesSentimentScores'])
                            done_scraping = row['DoneScraping'] == 'TRUE'
                            # load in primary articles data
                            for i in range(len(primary_articles_analyzed)):
                                article_link = primary_articles_analyzed[i]
                                article_sentiment = primary_articles_sentiment_scores[i]
                                stock_analyze_data.primary_articles_data += [(article_link, article_sentiment)]
                            # load in linking articles data
                            for i in range(len(linking_articles_analyzed)):
                                article_link = linking_articles_analyzed[i]
                                article_sentiment = linking_articles_sentiment_scores[i]
                                stock_analyze_data.linking_articles_data += [(article_link, article_sentiment)]
                            # load in connected stocks
                            for i in range(len(connected_companies)):
                                ticker, frequency = connected_companies[i], connected_frequencies[i]
                                stock_analyze_data.connected_tickers[ticker] = frequency
                            # update scraper
                            stock_analyze_data.scraper.articles_scraped = primary_articles_analyzed
                            stock_analyze_data.done_scraping = done_scraping
        # scrape for data if required
        if self._settings.output_info:
            print("Starting Web Scrape")
        # begin analysis
        progress = 0
        total_progress = len(self.analyzed_data)
        for ticker in self.analyzed_data:
            self._analyze_stock(ticker)
            progress += 1
            if self._settings.output_info:
                print("============================")
                print("PROGRESS [" + str(progress/total_progress * 100) + '%' + ']')
                print("============================")

        if self._settings.output_info:
            print("!==============!")
            print("DATA BUILD COMPLETE")
            print("!==============!")



    def __init__(self, tickers: list[str],
                 settings: StockAnalyzerSettings = StockAnalyzerSettings(id="Default", articles_per_ticker=5,
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
                self.analyzed_data[ticker] = StockAnalyzeData(
                    Stock(
                        name=stock_info['Name'],
                        ticker=stock_info['Symbol'],
                        market_cap=float(stock_info['Market Cap']),
                        industry=stock_info['Industry'],
                        sentiment=0,
                    ),
                    scraper=NewsScraper(
                        search_query=stock_info['Symbol'] + SEARCH_FOCUS[self._settings.search_focus],
                        number_of_articles=self._settings.articles_per_ticker,
                        publish_range=PUBLISH_RANGE[self._settings.articles_publish_range]
                    )
                )
            else:
                if self._settings.output_info:
                    print(ticker + ' was not found in the database')
        # build the scrape data
        self._build_data()
        # calculate stock attributes from scaped values
        for ticker in self.analyzed_data:
            analyze_data = self.analyzed_data[ticker]
            # calculate sentiment values
            # calculate the sentiment from primary articles
            primary_sentiment, linking_sentiment = 0, 0
            if len(analyze_data.primary_articles_data) > 0:
                # get median of sentiment data to avoid heavy influences from outliers.
                # also, since the data size is relatively small, median is the better choice in this case
                primary_sentiment = _get_median_sentiment_score(analyze_data.primary_articles_data)
            # calculate the sentiment from secondary articles
            if len(analyze_data.linking_articles_data) > 0:
                # ignore sentiment values of exactly 0 as it dilutes the overall sentiment
                linking_sentiment = _get_median_sentiment_score(analyze_data.linking_articles_data)
            # get sentiment value from combining linking sentiment and primary sentiment
            analyze_data.stock.sentiment = (primary_sentiment + linking_sentiment) / 2
