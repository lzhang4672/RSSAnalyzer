"""
File containing all methods for webscraping
"""

import random

import bs4
from python_ta.contracts import check_contracts
from bs4 import BeautifulSoup
import requests
import time

# constants
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.88 Safari/537.36"
}
SEARCH_PARAMS = {
    "hl": "en-US",  # language
    "gl": "US",  # country of the search, US -> USA
    "ceid": "US:en",
    "start": 10
}
NEWS_URL = "https://www.google.com/search"
WEB_TIMEOUT = 30

BS4OBJECT = bs4.element.NavigableString | bs4.element.Tag


@check_contracts
def get_articles(query: str, number_of_pages: int) -> None:
    """

    :param query:
    :param number_of_pages:
    """
    page_num = 0
    search_params = SEARCH_PARAMS
    # configure search params
    search_params["q"] = query + " stock"
    while page_num < number_of_pages:
        # sleep for an arbitrary amount to avoid rate limiting
        time.sleep(random.uniform(0.25, 1))
        html = requests.get(NEWS_URL, params=search_params, headers=HEADERS, timeout=30)
        soup = BeautifulSoup(html.text, "lxml")
        for result in soup.select(".WlydOe"):
            source = result.select_one(".NUnG9d").text
            title = result.select_one(".mCBkyc").text
            link = result.get("href")
            try:
                snippet = result.select_one(".GI74Re").text
            except AttributeError:
                snippet = None
            date = result.select_one(".ZE0LJd").text

            print(source, title, link, snippet, date, sep='\n', end='\n\n')
        if soup.select_one('.BBwThe'):
            search_params["start"] += 10
        else:
            break
        page_num += 1


@check_contracts
def get_texts_from_article(url: str) -> dict:
    """

    :param url:
    :param keywords:
    :return:
    """
    page = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(page.content, 'html.parser')

    tags = {'p'}
    content = soup.find_all(tags)
    website_info = {'title': soup.find('title'), 'texts': []}

    for passage in content:
        website_info['texts'].append(get_children_as_str(passage))

    return website_info


@check_contracts
def get_children_as_str(obj: BS4OBJECT) -> str:
    """
    Helper method for get_texts_containing
    Returns a string that concatenates the string elements inside the HTML tags based on the object passed in

    The bs4 object is a tree with a representation structure of the HTML of the website. This function will
    concatenate the elements inside the children of the object
    (ie. for <p>hello <strong>world</strong></p>, the object is the entire <p>, the children is the <strong> elem.)

    :param obj: A bs4 object that represents the HTML corresponding to a website
    :return:
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
    Strips non ascii values from the given string
    :param string: the string to remove non ascii from
    :return: returns new string with only ascii values
    """
    return ''.join([i if ord(i) < 128 else '' for i in string])
