"""
File for graphs generated based on a stock and functions related to navigatign the graph
"""
from Graph import Graph, CompanyNode, IndustryNode
from StockAnalyzer import StockAnalyzer
from StockInfo import get_info_from_ticker, get_tickers

class StockGraphAnalyzer:
    """
    A class for a graph generated based on a stock

    Instance Attributes:
        - graph: a graph object representing the associated graph for a stock
        - analyzer: a StockAnalyzer object that will hold the data needed to generate the graph's edges and nodes
    """
    graph: Graph
    analyzer: StockAnalyzer

    def __init__(self, stock_analyzer: StockAnalyzer) -> None:
        self.graph = Graph()
        self.analyzer = stock_analyzer

    def generate_graph(self) -> None:
        tickers = self.analyzer.tickers
        data = self.analyzer.get_data()
        # add all the company nodes first
        for ticker in tickers:
            ticker_info = get_info_from_ticker(ticker)
            self.graph.add_company_node(
                name=ticker_info['Name'],
                ticker=ticker,
                market_cap=ticker_info['Market Cap'],
                industry=ticker_info['Industry'],
                sentiment=
            )
