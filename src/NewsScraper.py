"""
File containing all methods for webscraping
"""

import random

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
    "start": 10,
    "tbm": "nws",
}
NEWS_URL = "https://www.google.com/search"
WEB_TIMEOUT = 30


@check_contracts
def get_articles(query: str, number_of_articles: int) -> list[str]:
    """Returns a list of article links as a string in a list.

    Preconditions:
        - query != ''
        - 0 < number_of_articles
    """
    articles = []
    number_of_articles_so_far = 0
    search_params = SEARCH_PARAMS
    # configure search params
    search_params["q"] = query + " stock"
    while number_of_articles_so_far < number_of_articles:
        # sleep for an arbitrary amount to avoid rate limiting
        time.sleep(random.uniform(0.25, 1))
        try:
            # try to send a request and retrieve the articles from google news
            html = requests.get(NEWS_URL, params=search_params, headers=HEADERS, timeout=30)
        except requests.exceptions.RequestException as e:
            # something went wrong so abort the program
            raise SystemExit(e)
        # parse the html using beautifulsoup
        soup = BeautifulSoup(html.text, "lxml")
        for result in soup.select(".WlydOe"):
            # get the article link by retrieving href tags.
            article_link = result.get("href")
            articles += [article_link]
            number_of_articles_so_far += 1
        if soup.select_one('.BBwThe'):
            search_params["start"] += 10
        else:
            break

    return articles


@check_contracts
def get_texts_from_article(url: str) -> dict[str, str | list[str]]:
    """
    Returns a dictionary specifying the title and texts in the article (two keys in the dictionary)
    Texts will be given in as a list of strings, and only <p> tags will be scraped to avoid too many texts. Note that
    any piece of text with only one word in it will NOT be included

    If this functions fails to fetch the url, an exception will be thrown

    Preconditions:
        - url must be a legal url
    """
    try:
        # try to send a request and retrieve the article
        page = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        # something went wrong so abort the program
        raise SystemExit(e)

    soup = BeautifulSoup(page.content, 'html.parser')

    tags = {'p'}
    content = soup.find_all(tags)
    website_info = {'title': str(soup.find('title').string), 'texts': []}

    for passage in content:
        string = get_children_as_str(passage)
        if len(string.split()) > 1:  # has more than just 1 word
            website_info['texts'].append(string)

    return website_info


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
