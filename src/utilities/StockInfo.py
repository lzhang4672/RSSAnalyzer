from python_ta.contracts import check_contracts
import csv
from CSV import csv_reader

tickers = csv_reader('tickers_data.csv')

def get_name(ticker):
    return tickers[ticker]['name']

def get_industry(ticker):
    return tickers[ticker]['industry']

def get_market_cap(ticker):
    return tickers[ticker]['market cap']


