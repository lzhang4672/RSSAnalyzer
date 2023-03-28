"""
Graph
"""


@check_contracts
class Node:
    """
    Abstract class for all nodes in the graph

    Instance Attributes:
        - name: name of the stock/company or industry
        - sentiment: a float between -10 to 10 representing the sentiment of the stock or industry
        - neighbours: nodes connected to self
    """
    name: str
    sentiment: float
    edges: list[Node]

    def __init__(self, name: str, sentiment: float) -> None:
        self.name = name
        self.sentiment = sentiment


@check_contracts
class CompanyNode(Node):
    """
    A class representing a company/stock

    Instance Attributes:
        - ticker: the ticker for the stock
        - market_cap: market capitalization of the company (how much the company is worth in billions)
        - industry: the industry the company is in
    """
    ticker: str
    market_cap: float
    industry: str

    def __init__(self, name: str, sentiment: float, ticker: str, market_cap: float, industry: str) -> None:
        super().__init__(name, sentiment)
        self.ticker = ticker
        self.market_cap = market_cap
        self.industry: industry


class IndustryNode(Node)
