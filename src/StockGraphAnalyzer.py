"""
File for graphs generated based on a stock and functions related to navigatign the graph
"""
from Graph import Graph, CompanyNode, IndustryNode, Edge, Node
from StockAnalyzer import StockAnalyzer
from StockInfo import get_info_from_ticker, get_tickers
from collections import deque
from dataclasses import dataclass


@dataclass
class IndustryData:
    """
    Dataclass to keep track of temporary data for an IndustryNode
    """
    tickers: list[str]
    sentiment: list[float]
    market_cap: float

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
        data = self.analyzer.analyzed_data
        industries = {}

        # add all the company nodes first
        # NOTE: for sentiment parameter: calculates the average sentiment based on the articles scraped
        #     Essentially, StockAnalyzeData.primary_articles_data stores a list of tuples corresponding to
        #     (url, sentiment from that url), so this private function will calculate average overall sentiment
        #     based off of a StockAnalyzeData object
        for ticker in tickers:
            if ticker in data:
                ticker_analyzed_data = data[ticker]
                ticker_stock = ticker_analyzed_data.stock
                new_node = CompanyNode(
                    name=ticker_stock.name,
                    ticker=ticker,
                    market_cap=ticker_stock.market_cap,
                    industry=ticker_stock.industry,
                    sentiment=ticker_stock.sentiment
                )
                self.graph.add_company_node(new_node)

            # will be used when adding industry nodes to graph
            # note that new_node.sentiment * new_node.market_cap allows me to weigh the overall sentiment for industry
            # based on the market cap
            if ticker_info['Industry'] not in industries:
                industries[ticker_info['Industry']] = IndustryData(tickers=[ticker],
                                                                   sentiment=[new_node.sentiment * new_node.market_cap],
                                                                   market_cap=new_node.market_cap)
            else:
                industries[ticker_info['Industry']].tickers.append(ticker)
                industries[ticker_info['Industry']].sentiment.append(new_node.sentiment * new_node.market_cap)
                industries[ticker_info['Industry']].market_cap += new_node.market_cap

        # add edge to neighbouring nodes; weigh the edges based on frequency
        created_edges = set()
        for ticker in tickers:
            connected = data[ticker].connected_tickers
            for neighbour in connected:
                if (ticker, neighbour) not in created_edges and (neighbour, ticker) not in created_edges:
                    if ticker in data[neighbour].connected_tickers:
                        other_freq = float(data[neighbour].connected_tickers[ticker])
                    else:
                        other_freq = 0.0
                    # print(ticker, neighbour, connected[neighbour], other_freq)
                    self.graph.add_edge(ticker, neighbour, float(connected[neighbour]), other_freq)

        # add industry nodes
        for industry in industries:
            values = industries[industry]
            sentiment = sum(values.sentiment) / values.market_cap
            self.graph.add_industry_node(industry, values.market_cap, sentiment)
            # add edges to industry node (connect to tickers)
            # edge weight based on market cap / total market cap (how big of a % does the ticker hold)
            for index in range(len(values.tickers)):
                ticker, weight = values.tickers[index], values.sentiment[index] / values.market_cap
                # from ticker back to industry, the weight will be 0
                self.graph.add_edge(industry, ticker, weight, 0.0)

    def get_industry_connectivity(self) -> dict[str, float]:
        """
        Returns how well each industry node connects to other industry nodes based on the edges that cross
        connect the nodes from the different industries

        Preconditions:
            - Assumes the graph has already added all edges for CompanyNodes
        """

    def get_best_neighbour(self, node: Node) -> Node | None:
        """
        Returns the best neighbouring node to the node given.
        If the node is not connected to any other nodes, or all connected nodes have a lower sentiment, returns None
        """

    def find_community(self) -> set[list[Node]]:
        """
        Returns a set of lists. Each list is a set
        """

    def _get_edge_highest_betweenness(self) -> list[Edge]:
        """
        Private helper method for finding communities
        Returns the edge(s) with the highest "between-ness" as per the Girvan Newman Algorithm
        """
        node1 = self.graph.nodes['NKE']
        node2 = self.graph.nodes['UAA']
        print(node1, node2)
        print(self.find_best_path(node1, node2))

    def rank_node_importance(self) -> list[Node]:
        """
        Returns a list in sorted order of the "importance" of the nodes
        Importance score is calculated based on how many cross-references it has
        """

    def find_best_path(self, cur_node: Node, end_node: Node) -> list[Edge] | None:
        """
        Returns the EDGES traversed by the shortest path to end_node from start_node, otherwise returns none if it
        doesn't exist. This will be used as a helper function for StockGraphAnalyzer._get_edge_betweenness
        Uses kruskal's algorithm to manage weighed edges. Edges are sorted based on average weight
        """
        queue = deque([edge for edge in cur_node.edges])
        edges = set()
        sorted_edges = sorted([edge for edge in self.graph.edges], key=lambda edge: edge.get_average_weight())
        roots = {key: key for key in self.graph.nodes}
        for edge in sorted_edges:
            node1, node2 = edge.u, edge.v

    def _root(self, node: str, roots: dict[str, str]) -> str:
        """
        Helper for find_best_path

        Searches for and returns the "root" of a node. This will help with checking if two nodes are connected
        During the searching process, modifies "root" dict/disjoint set to keep track of cycles
        """
        while roots[node] != node:
            roots[node] = roots[roots[node]]
            node = root[node]
        return node

    def _union(self, node1: str, node2: str, roots: dict[str, str]) -> None:
        """
        Links two nodes together, bascially "union" for a disjoint set
        """
        rootA, rootB = self._root(node1, roots), self._root(node2, roots)
        roots[rootA] = roots[rootB]




# for testing
if __name__ == '__main__':
    from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings

    default_settings = StockAnalyzerSettings(id='all_tickers', articles_per_ticker=20, use_cache=True,
                                             search_focus='Competitors')
    tickers = get_tickers()
    analyzer = StockAnalyzer(tickers, default_settings)

    sg = StockGraphAnalyzer(analyzer)
    sg.generate_graph()
    sg._get_edge_highest_betweenness()
