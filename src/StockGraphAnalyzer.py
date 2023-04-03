"""
File for graphs generated based on a stock and functions related to navigating the graph

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and professors
 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult the Course Syllabus.

This file is Copyright (c) 2023 Mark Zhang, Li Zhang and Luke Zhang
"""
from Graph import Graph, CompanyNode, IndustryNode, Edge, Node
from StockAnalyzer import StockAnalyzer
from StockInfo import get_info_from_ticker, get_tickers
from collections import deque
from dataclasses import dataclass
from typing import Optional


@dataclass
class IndustryData:
    """
    Dataclass to keep track of temporary data for an IndustryNode

    Instance Attributes:
        - tickers: a list containing all the tickers that fall under this industry
        - sentiment: a list containing weighted sentiment of each
        - market_cap: a list containing all the market cap values for the ticker
        - industry_cap: the total industry cap, calculated by the sum of all market caps of the tickers

    Representations Invariants:
        - self.tickers list corresponds to self.sentiment and self.market_cap by index,
        ie. at the i-th index, the i-th index in sentiment is the sentiment weight for the i-th ticker and
        the i-th index in market_cap is the market cap for the i-th ticker in tickers
    """
    tickers: list[str]
    sentiment: list[float]
    market_cap: list[float]
    industry_cap: float


class StockGraphAnalyzer:
    """
    A class for a graph generated based on a stock

    Instance Attributes:
        - graph: a graph object representing the associated graph for a stock
        - analyzer: a StockAnalyzer object that will hold the data needed to generate the graph's edges and nodes
        - pagerank_scores: a dictionary with the pagerank score correspodning to the CompanyNode
        - ordered_node_sentiment_scores: a list containing the ordered sentiment tickers
        - ordered_pagerank_scores: a list containing the ordered pagerank tickers

    Representation Invariants:
        - len(self.graph.nodes) == len(self.pagerank_scores)
    """
    graph: Graph
    analyzer: StockAnalyzer
    pagerank_scores: dict[CompanyNode, float]
    ordered_pagerank_scores: list[str] = []
    ordered_node_sentiment_scores: list[str] = []

    def __init__(self, stock_analyzer: StockAnalyzer) -> None:
        self.graph = Graph()
        self.analyzer = stock_analyzer
        self.pagerank_scores = {}

    def generate_graph(self) -> None:
        """
        Generates the graph based on data from self.analyzer
        """
        all_tickers = self.analyzer.tickers
        data = self.analyzer.analyzed_data
        industries = {}

        # add all the company nodes first
        # NOTE: for sentiment parameter: calculates the average sentiment based on the articles scraped
        #     Essentially, StockAnalyzeData.primary_articles_data stores a list of tuples corresponding to
        #     (url, sentiment from that url), so this private function will calculate average overall sentiment
        #     based off of a StockAnalyzeData object
        for ticker in all_tickers:
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
                # note that new_node.sentiment * new_node.market_cap allows me to weigh the overall sentiment for
                # industry based on the market cap
                if ticker_stock.industry not in industries:
                    industries[ticker_stock.industry] = IndustryData(tickers=[ticker],
                                                                     sentiment=[new_node.sentiment *
                                                                                new_node.market_cap],
                                                                     market_cap=[new_node.market_cap],
                                                                     industry_cap=new_node.market_cap)
                else:
                    industries[ticker_stock.industry].tickers.append(ticker)
                    industries[ticker_stock.industry].sentiment.append(new_node.sentiment * new_node.market_cap)
                    industries[ticker_stock.industry].market_cap.append(new_node.market_cap)
                    industries[ticker_stock.industry].industry_cap += new_node.market_cap

        # add edge to neighbouring nodes; weigh the edges based on frequency
        created_edges = set()
        for ticker in all_tickers:
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
            sentiment = sum(values.sentiment) / values.industry_cap
            new_node = IndustryNode(industry, values.industry_cap, sentiment)
            self.graph.add_industry_node(new_node)
            # add edges to industry node (connect to tickers)
            # edge weight based on market cap / total market cap (how big of a % does the ticker hold)
            for index in range(len(values.tickers)):
                ticker, weight = values.tickers[index], values.market_cap[index] / values.industry_cap
                # from ticker back to industry, the weight will be 0
                self.graph.add_edge(industry, ticker, weight, 0.0)

        # store a ranking of highest sentiment to lowest
        all_nodes = self.graph.nodes
        self.ordered_node_sentiment_scores = \
            sorted([node for node in all_nodes], key=lambda sort_node: self.graph.nodes[sort_node].sentiment,
                   reverse=True)

    def get_best_neighbour(self, node: Node) -> Node | None:
        """
        Returns the best neighbouring node to the node given.
        If the node is not connected to any other nodes, or all connected nodes have a lower sentiment, returns None

        Preconditions:
            - the graph has already been constructed (otherwise, this function is guaranteed to return None since the
            nodes won't have neighbours)
        """
        if len(node.neighbour) == 0:
            return None
        best, best_sentiment = None, node.sentiment
        for neighbour in node.neighbour:
            if isinstance(neighbour, IndustryNode):
                continue
            elif neighbour.sentiment > best_sentiment:
                best, best_sentiment = neighbour, neighbour.sentiment
        return best

    def _run_pagerank_algorithm(self, depth: Optional[int]) -> None:
        """
        Returns a dictionary mapping a node (represented by its name or ticker) to it's pagerank score.
        Pagerank algorithm based on the simple version from wikipedia:
        https://en.wikipedia.org/wiki/PageRank#Simplified_algorithm
        In a nutshell, this algorithm gives the importance of nodes through determining how many "other" connections
        the nodes have. Consider arbitrary nodes A and B inside the graph, and suppose they are connected. Also,
        suppose we know A and B are connected, but A is ONLY connected to B, whereas B is connected to other nodes
        other than A. In pagerank algorithm, B would be MORE important to A (since it is A's ONLY connection), but A
        is not as important to B.

        Preconditions:
            - the graph has already been generated
        """
        all_nodes = set(self.graph.nodes.values())
        for node in all_nodes:
            score = node.get_pr_score()
            if depth is not None:
                linked_nodes = self._get_linked_nodes(node, depth)
            else:
                linked_nodes = self._get_linked_nodes(node, 1)
            for linked_node in linked_nodes:
                if linked_node in self.pagerank_scores:
                    self.pagerank_scores[linked_node] += score
                else:
                    self.pagerank_scores[linked_node] = score
        # store ordered stocks based on pagerank
        all_nodes = set(self.pagerank_scores.keys())
        self.ordered_pagerank_scores = \
            sorted([node for node in all_nodes], key=lambda sort_node: self.pagerank_scores[sort_node], reverse=True)

    def run_preprocessed_algorithms(self) -> None:
        """
        Runs all the preprocessed algorithms associated with the graph
        """
        self._run_pagerank_algorithm(8)

    def _get_linked_nodes(self, given_node: Node, depth: int) -> set[str]:
        """
        Returns all nodes connected to given node, not in any particular order
        Uses BFS with depth, -> gets the connected nodes within the depth parameter away.

        Preconditions:
            - the graph has already been generated
        """
        queue = deque([given_node])
        visited = {given_node.get_as_key()}
        depth_counter = 0
        while queue and depth_counter < depth:
            for _ in range(len(queue)):
                cur = queue.popleft()
                for neighbour in cur.neighbours:
                    if neighbour.get_as_key() not in visited:
                        queue.append(neighbour)
                        visited.add(neighbour.get_as_key())
            depth_counter += 1
        return visited


# for testing
if __name__ == '__main__':
    from StockAnalyzer import StockAnalyzer, StockAnalyzerSettings

    default_settings = StockAnalyzerSettings(id='all_tickers_10_articles', articles_per_ticker=10, use_cache=True,
                                             search_focus='Stock')
    tickers = get_tickers()
    analyzer = StockAnalyzer(tickers, default_settings)

    sg = StockGraphAnalyzer(analyzer)
    sg.generate_graph()
    print('generated graph')
    print(len(sg.graph.nodes))
    d = sg.pagerank()
    print(d)
    ranks = sg.get_ordered_neighbours(sg.graph.get_node_by_name('RBLX'))
    print('======')
    print(ranks)

    # n1 = CompanyNode('Roblox', 'RBLX', 123.4, 'Technology', 5.0)
    # n2 = CompanyNode('Microsoft', 'MSFT', 123.4, 'Technology', 4.0)
    # print(isinstance(n1, CompanyNode))
