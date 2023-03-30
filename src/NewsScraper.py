"""
File containing all methods for webscraping
"""

import random
from dataclasses import dataclass, field
import bs4
from python_ta.contracts import check_contracts
from bs4 import BeautifulSoup
import requests
import time

# == CONSTANTS ==
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.88 Safari/537.36"
}

SEARCH_PARAMS = {
    "hl": "en-US",  # language
    "gl": "US",  # country of the search, US -> USA
    "ceid": "US:en",
    "start": 0,
    "tbm": "nws",
    "tbs": "qdr:",
}
NEWS_URL = "https://www.google.com/search"
WEB_TIMEOUT = 30


PUBLISH_RANGE = {
    'PastYear': 'y',
    'PastMonth': 'm',
    'PastWeek': 'w',
    'PastDay': 'd',
    'Recent': '',
}

@dataclass
class NewsArticleContent:
    """A dataclass to represent the content of a news article

    Instance Attributes:
        - title: a string representing the title of the article
        - url: a string representing the link to the news article.

    Representation Invariants:
        - url is in the format of a web url
    """
    title: str
    paragraphs: list[str]


def get_content_from_article_url(url: str) -> NewsArticleContent | None:
    """
    Returns a NewsArticleContentObject that contains the content for the article
    Texts will be given in as a list of strings, and only <p> tags will be scraped to avoid too many texts. Note
    that any piece of text with only one word in it will NOT be included

    If this functions fails to fetch the url, return nothing

    Preconditions:
        - news_article.url is a legal url.
    """
    texts = []
    try:
        # try to send a request and retrieve the article
        page = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        # something went wrong so return nothing
        return None

    soup = BeautifulSoup(page.content, 'html.parser')

    tags = {'p'}
    title = str(soup.find('title').string)
    content = soup.find_all(tags)

    for passage in content:
        string = get_children_as_str(passage)
        if len(string.split()) > 1:  # has more than just 1 word
            texts += [string]

    return NewsArticleContent(
        title=title,
        paragraphs=texts
    )


class NewsScraper:
    """This class will handle the scraping process

     Instance Attributes:
        - search_query: a string representing what search query to use when scraping for articles.
        - number_of_articles: an integer representing the number of articles to scrape.
        - articles_scraped: a list containing the urls of the news articles scraped.
        - publish_range: a string representing how recent the articles should be when being scraped.

    """
    search_query: str
    number_of_articles: int
    articles_scraped: list[str]
    publish_range: str

    def scrape_articles(self) -> bool:
        """Scrapes the specified amount of articles stated in self.number_of_articles
        Returns true of the scraping was successful, false otherwise.

        Preconditions:
            - query != ''
            - 0 < number_of_articles
        """
        number_of_articles_so_far = 0
        # configure search params
        SEARCH_PARAMS['start'] = 0
        SEARCH_PARAMS['q'] = self.search_query
        SEARCH_PARAMS['tbs'] = "qdr:" + self.publish_range
        while number_of_articles_so_far < self.number_of_articles:
            # sleep for an arbitrary amount to avoid rate limiting
            time.sleep(random.uniform(0.25, 1))
            try:
                # try to send a request and retrieve the articles from Google News
                html = requests.get(NEWS_URL, params=SEARCH_PARAMS, headers=HEADERS, timeout=30)
            except requests.exceptions.RequestException as e:
                # something went wrong so abort the program
                return False
            # parse the html using beautifulsoup
            soup = BeautifulSoup(html.text, "lxml")
            for result in soup.select(".WlydOe"):
                # get the article link by retrieving href tags.
                article_link = result.get("href")
                if article_link not in self.articles_scraped:
                    self.articles_scraped += [article_link]
                    number_of_articles_so_far += 1
            if soup.select_one('.BBwThe'):
                SEARCH_PARAMS["start"] += 10
            else:
                break

        return True

    def get_articles(self) -> list[str]:
        """
        Returns the url of the articles scraped
        """
        return self.articles_scraped

    def __init__(self, search_query: str, number_of_articles: int, publish_range: str):
        """Constructor for a NewsScraper object

            Preconditions:
                - search_query != ''
                - 0 < number_of_articles
                - any(PUBLISH_RANGE[range] == publish_range for range in PUBLISH_RANGE)
        """
        self.search_query = search_query
        self.number_of_articles = number_of_articles
        self.publish_range = publish_range
        self.articles_scraped = []


@check_contracts
def get_children_as_str(obj: bs4.element.NavigableString | bs4.element.Tag) -> str:
    """
    Helper method for get_texts_containing
    Returns a string that concatenates the string elements inside the HTML tags based on the object passed in

    The bs4 object is a tree with a representation structure of the HTML of the website. This function will
    concatenate the elements inside the children of the object
    (ie. for <p>hello <strong>world</strong></p>, the object is the entire <p>, the children is the <strong> elem.)

    Preconditions:
        - obj is a bs4 object that represents the HTML corresponding to a website
    """
    if isinstance(obj, bs4.NavigableString):
        return remove_non_ascii(str(obj))
    else:
        cur_str = ''
        for child in obj.children:
            cur_str += get_children_as_str(child)
        return cur_str


@check_contracts
def remove_non_ascii(string: str) -> str:
    """
    Helper method for get_children_as_str, and for handling strings
    Strips non ascii values from the given string and returns a new string without the values
    """
    return ''.join([i if ord(i) < 128 else '' for i in string])
