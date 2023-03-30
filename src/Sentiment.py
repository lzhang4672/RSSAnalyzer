from __future__ import annotations
from typing import Optional
import openai
from python_ta.contracts import check_contracts
from NewsScraper import NewsArticleContent
from dataclasses import dataclass, field
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import StockInfo


# fin-bert model
finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
get_sentiment = pipeline("text-classification", model=finbert, tokenizer=tokenizer)

# model constants
openai.api_key = "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"
model_engine = "gpt-3.5-turbo"
SET_UP_PROMPT = "Give a sentiment score from -10 to 10 for each company " \
                "in a " \
                "dictionary format. Do NOT provide any other output. Output \"ERROR\" on any errors.\n"
MAX_TOKENS = 250





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


def get_complex_phrase_sentiment_score(passage: str) -> dict[str, float]:
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


def stocks_in_passage(passage: str) -> set:
    """
    Returns a set containing all the stocks mentioned in the passage as a ticker
    """
    print(get_sentiment(passage))
    stocks_mentioned = set()
    words = passage.split()
    tickers, names = StockInfo.get_tickers_and_names()

    for word in words:
        if word in tickers:
            stocks_mentioned.add(word)
        elif word in names:
            stocks_mentioned.add(StockInfo.get_ticker_from_name(word))

    return stocks_mentioned


def get_sentiment_for_article(main_stock: Stock, news_article: NewsArticle, content: list[str]) -> ArticleSentimentData:
    """
    Returns sentiment data for an article
    """
    title_stocks = stocks_in_passage(news_article.title)
    title_stock_score = 0
    sentiment_data = {}
    if len(title_stocks) > 1:
        sentiment_data.update(get_complex_phrase_sentiment_score(news_article.title))
    else:
        sentiment_data[title_stocks.pop()] = get_sentiment_single(news_article.title)
    if main_stock.ticker in sentiment_data:
        title_stock_score = sentiment_data.pop(main_stock.ticker)  # don't want main stock to be in other stocks dict

    passage_stock_score = 0
    for passage in content:
        passage_stocks = stocks_in_passage(passage)
        if len(passage_stocks) > 1:
            passage_stocks_sentiment = get_complex_phrase_sentiment_score(passage)
            for stock in passage:
                if stock in sentiment_data:
                    sentiment_data[stock] = (sentiment_data[stock] + passage_stocks_sentiment[stock]) / 2
                else:
                    sentiment_data[stock] = passage_stocks_sentiment[stock]
        else:
            sentiment_data[passage_stocks.pop()] = get_sentiment_single(passage)
        if main_stock.ticker in sentiment_data:
            passage_stock_score += sentiment_data.pop(main_stock.ticker)

    # adjustment for main stock - title is more heavily weighted
    main_stock_score = (title_stock_score * 0.6) + (passage_stock_score * 0.4) / len(content)
    # adjustment for other stocks since the article is not primarly focused on the other stocks, make it weigh
    # slightly less
    for stock in sentiment_data:
        sentiment_data[stock] *= 0.8
    return ArticleSentimentData(main_sentiment_score=main_stock_score, other_sentiment_scores=sentiment_data)
