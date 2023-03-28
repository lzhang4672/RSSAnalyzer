import random

from python_ta.contracts import check_contracts
from bs4 import BeautifulSoup
import requests
import time

# constants
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
}
SEARCH_PARAMS = {
    "hl": "en-US",  # language
    "gl": "US",  # country of the search, US -> USA
    "ceid": "US:en",
    "start": 10
}
NEWS_URL = "https://www.google.com/search"
WEB_TIMEOUT = 30


@check_contracts
class NewsScraper:
    """
    class for news web scraping
    """

    @staticmethod
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

    @staticmethod
    def get_texts_containing(url: str, tickers: list) -> list[str]:
        """

        :param url:
        :param tickers:
        :return:
        """
        page = requests.get(url, headers=HEADERS)

        soup = BeautifulSoup(page.content, 'html.parser')

        texts_so_far = []
        tags = {'p'}
        content = soup.find_all(tags)

        for text in content:
            string = str(text)
            for ticker in tickers:
                if ticker in string:
                    texts_so_far.append(get_children_as_str(text))
        return texts_so_far
