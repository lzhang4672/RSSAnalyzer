"""
File containing the nodes and graphs to represent the stocks

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mark Zhang, Li Zhang and Luke Zhang
"""


@check_contracts
class Node:
    """
    Abstract class for all nodes in the graph

    Instance Attributes:
        - name: name of the stock/company or industry
        - neighbours: nodes connected to self
    """
    name: str
    edges: list[Node]

    def __init__(self, name: str) -> None:
        self.name = name
        self.edges = []


@check_contracts
class CompanyNode(Node):
    """
    A class representing a company/stock

    Instance Attributes:
        - ticker: the ticker for the stock
        - market_cap: market capitalization of the company (how much the company is worth in billions)
        - industry: the industry the company is in
        - sentiment: the sentiment rating between -10 to 10, associated with the stock

    Preconditions:
        - -10 <= self.sentiment <= 10
    """
    ticker: str
    market_cap: float
    industry: str
    sentiment: float

    def __init__(self, name: str, ticker: str, market_cap: float, industry: str, sentiment: float) -> None:
        super().__init__(name)
        self.ticker = ticker
        self.market_cap = market_cap
        self.industry: industry
        self.sentiment = sentiment


@check_contracts
class IndustryNode(Node):
    """
    A class representing an industry

    Instance Attributes:
        - market_cap: total worth of the industry, the sum of all market caps of companies in the industry
        - sentiment: the sentiment rating from -10 to 10 of the entire industry, calculated from averaging all the
        sentiments of companies in the industry.

    Preconditions:
        - -10 <= self.sentiment <= 10
    """
    market_cap: float
    sentiment: float

    def __init__(self, name: str, market_cap: float, sentiment: float):
        super().__init__(name)
        self.market_cap = market_cap
        self.sentiment = sentiment


class Edge:
    """
    A class representing the edge of the graph

    Note with caution that this edge is bi-weighted

    Instance Attributes:
        - u: a Node on one end of this edge
        - v: another Node on the other end of this edge
        - u_v_weight: weight for the edge going from u to v
        - v_u_weight: weight for edge going from v to u
    """
    u: IndustryNode | CompanyNode
    v: IndustryNode | CompanyNode
    u_v_weight: float
    v_u_weight: float
