"""
File for graphs generated based on a stock and functions related to navigatign the graph
"""
from Graph import Graph, CompanyNode, IndustryNode, Edge, Node
from StockAnalyzer import StockAnalyzer
from StockInfo import get_info_from_ticker, get_tickers
from collections import deque


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
        data = self.analyzer.analyze_data
        industries = {}

        # add all the company nodes first
        # NOTE: for sentiment parameter: calculates the average sentiment based on the articles scraped
        #     Essentially, StockAnalyzeData.primary_articles_data stores a list of tuples corresponding to
        #     (url, sentiment from that url), so this private function will calculate average overall sentiment
        #     based off of a StockAnalyzeData object
        for ticker in tickers:
            ticker_info = get_info_from_ticker(ticker)
            if len(data[ticker].primary_articles_data) == 0:
                primary_sentiment = 0
            else:
                primary_sentiment = sum(float(i[1]) for i in data[ticker].primary_articles_data) / \
                                    len(data[ticker].primary_articles_data)
            if len(data[ticker].linking_articles_data) == 0:
                relational_sentiment = 0
            else:
                relational_sentiment = sum(float(i[1]) for i in data[ticker].linking_articles_data) / \
                                       len(data[ticker].linking_articles_data)
            new_node = CompanyNode(
                name=ticker_info['Name'],
                ticker=ticker,
                market_cap=float(ticker_info['Market Cap']),
                industry=ticker_info['Industry'],
                sentiment=primary_sentiment * 0.8 + relational_sentiment * 0.2
            )
            self.graph.add_company_node(new_node)

            # will be used when adding industry nodes to graph
            # note that new_node.sentiment * new_node.market_cap allows me to weigh the overall sentiment for industry
            # based on the market cap
            if ticker_info['Industry'] not in industries:
                industries[ticker_info['Industry']] = [[ticker], [new_node.sentiment * new_node.market_cap],
                                                       new_node.market_cap]
            else:
                industries[ticker_info['Industry']][0].append(ticker)
                industries[ticker_info['Industry']][1].append(new_node.sentiment * new_node.market_cap)
                industries[ticker_info['Industry']][2] += new_node.market_cap

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
            sentiment = sum(values[1]) / values[2]
            self.graph.add_industry_node(industry, values[2], sentiment)
            # add edges to industry node (connect to tickers)
            # edge weight based on market cap / total market cap (how big of a % does the ticker hold)
            for index in range(len(values[0])):
                ticker, weight = values[0][index], values[1][index] / values[2]
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
        print(dfs(node1, node2, {node1}))

    def rank_node_importance(self) -> list[Node]:
        """
        Returns a list in sorted order of the "importance" of the nodes
        Importance score is calculated based on how many cross-references it has
        """


def bfs(cur_node: Node, end_node: Node) -> set | None:
    """
    Returns the shortest path to end_node from start_node, otherwise returns none if it doesn't exist
    This will be used as a helper function for StockGraphAnalyzer._get_edge_betweenness

    """
    queue = deque([cur_node])
    while queue:
        for i in range(len(queue)):
            path = queue.popleft()
            if path[-1] is end_node:
                return lst
            for neighbour in path[-1].neighbours:



if __name__ == '__main__':
    from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings

    default_settings = StockAnalyzerSettings(id='all_tickers', articles_per_ticker=20, use_cache=True,
                                             search_focus='Competitors')
    tickers = get_tickers()
    analyzer = StockAnalyzer(tickers, default_settings)

    sg = StockGraphAnalyzer(analyzer)
    sg.generate_graph()
    sg._get_edge_highest_betweenness()
