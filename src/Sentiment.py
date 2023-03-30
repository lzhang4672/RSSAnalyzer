from __future__ import annotations
from typing import Optional

import openai
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from python_ta.contracts import check_contracts
from NewsScraper import NewsArticle
import StockInfo

# model constants
openai.api_key = "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"
model_engine = "gpt-3.5-turbo"
SET_UP_PROMPT = "Give a sentiment score from -10 to 10 for each company " \
                "in a " \
                "dictionary format. Do NOT provide any other output. Output \"ERROR\" on any errors.\n"
MAX_TOKENS = 250

sentiment_analyzer = SentimentIntensityAnalyzer()




@dataclass
class ArticleSentimentData:
    """A dataclass represetning the data returned by sentiment

    Instance Attributes:
        - main_sentiment_score: a float -10 <= x <= 10. This score represents the main stock's sentiment
        - other_sentiment_scores: a dictionary representing other stocks mentioned in the article corresponding to
                                  their sentiment.
    """

    main_sentiment_score: float
    other_sentiment_scores: dict[str, float]

def get_complex_phrase_sentiment_score(passage: str) -> None:
    """
    Used when retrieving the sentiment scores of multiple companies in a singular sentence/paragraph.
    """
    nlk_score = sentiment_analyzer.polarity_scores(passage)
    if nlk_score['neu'] < 0.5 or nlk_score["neg"] > 0.1 or nlk_score["pos"] > 0.1:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[{"role": "system", "content": SET_UP_PROMPT + passage}],
            max_tokens=MAX_TOKENS,
            temperature=0,
            stop=None,
        )
        #
        print(response.choices[0].message.content)
    else:
        print(nlk_score)
        print("too neutral")


def get_sentiment_single(passage: str) -> float:
    """
    Returns the sentiment score for a passage ASSUMING THERE IS ONLY ONE STOCK MENTIONED IN THE PASSAGE
    Uses ntlk's VADER

    Preconditions:
        - there is only ONE stock in the passage
    """
    # clean text by filtering out words that typically do not carry much meaning such as "and","the", "of"
    # removing this "fluff" may improve accuracy, but also may not, hence this function will average it
    stop_words = stopwords.words("english")
    cleaned_text = ' '.join([word for word in passage.split() if word not in stop_words])

    # return sentiment of the passage which is the average compound scores for the raw passage and the cleaned one
    cleaned_score = sentiment_analyzer.polarity_scores(cleaned_text)['compound']
    raw_score = sentiment_analyzer.polarity_scores(passage)['compound']
    return (cleaned_score + raw_score) * 5


def stocks_in_passage(passage: str) -> tuple[int, set]:
    """
    Returns a dictionary mapping stock mentioned to the number of times mentioned
    """
    stocks_mentioned, counter = set(), 0
    words = passage.split()
    tickers, names = StockInfo.get_tickers_and_names()

    for word in words:
        if word in tickers or word in names:
            counter += 1
            stocks_mentioned.add(word)

    return counter, stocks_mentioned



def get_sentiment_for_article(news_article: NewsArticle, content: list[str]) -> ArticleSentimentData:
    """
        Do some math calculations. Weight the news_article title the heaviest. Weight the other stocks mentioned
        a little less.
    """



def get_sentiment_for_multiple(passge: str) -> float:
    """
    Uses OpenAI
    """
    pass
