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
        """
        Generates the graph based on data from self.analyzer
        """
        tickers = self.analyzer.tickers
        data = self.analyzer.get_data()

        # add all the company nodes first
        # NOTE: for sentiment parameter: alculates the average sentiment based on the articles scraped
        #     Essentially, StockAnalyzeData.primary_articles_data stores a list of tuples corresponding to
        #     (url, sentiment from that url), so this private function will calculate average overall sentiment
        #     based off of a StockAnalyzeData object
        for ticker in tickers:
            ticker_info = get_info_from_ticker(ticker)
            self.graph.add_company_node(
                name=ticker_info['Name'],
                ticker=ticker,
                market_cap=ticker_info['Market Cap'],
                industry=ticker_info['Industry'],
                sentiment=sum(i[0] for i in data[ticker].primary_articles_data) / len(data[ticker])
            )

        # add edge to neighbouring nodes; weigh the edges based on frequency
        for ticker in tickers:
            connected = data[ticker].connected_tickers
            for neighbour in connected:
                self.graph.add_edge(ticker, neighbour, connected[neighbour])

        # add industry nodes
        for
    def get_industry_connectivity(self):
