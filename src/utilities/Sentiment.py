from __future__ import annotations
from typing import Optional

import openai
from nltk.sentiment import SentimentIntensityAnalyzer
from python_ta.contracts import check_contracts

# model constants
openai.api_key = "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"
model_engine = "gpt-3.5-turbo"
SET_UP_PROMPT = "Give a sentiment score from -10 to 10 for each company " \
                "in a " \
                "dictionary format. Do NOT provide any other output. Output \"ERROR\" on any errors.\n"
MAX_TOKENS = 250

sentiment_analyzer = SentimentIntensityAnalyzer()


class Sentiment:
    @staticmethod
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
