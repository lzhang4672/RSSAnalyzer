"""
File containing the nodes and graphs to represent the stocks

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and professors
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
        - edges: edges connected to this node

    Representation Invariants:
        - self.name != ''
    """
    name: str
    edges: set[Edge]

    def __init__(self, name: str) -> None:
        self.name = name
        self.edges = set()


@check_contracts
class CompanyNode(Node):
    """
    A class representing a company/stock. CompanyNode stores the associated industry it falls under

    Instance Attributes:
        - ticker: the ticker for the stock
        - market_cap: market capitalization of the company (how much the company is worth in billions)
        - industry: the industry the company is in
        - sentiment: the sentiment rating between -10 to 10, associated with the stock

    Representation Invariants:
        - self.ticker != ''
        - 0 < self.market_cap
        - self.industry != ''
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
    A class representing an industry. IndustryNodes may have multiple CompanyNodes connected to it, given that the
    company is under the industry

    Instance Attributes:
        - industry_cap: total worth of the industry, the sum of all market caps of companies in the industry
        - sentiment: the sentiment rating from -10 to 10 of the entire industry, calculated from averaging all the
        sentiments of companies in the industry.

    Representation Invariants:
        - 0 < self.industry_cap
        - -10 <= self.sentiment <= 10
    """
    industry_cap: float
    sentiment: float

    def __init__(self, name: str, industry_cap: float, sentiment: float):
        super().__init__(name)
        self.industry_cap = industry_cap
        self.sentiment = sentiment


class Edge:
    """
    A class representing the edge of the graph

    Note that this edge is bi-weighted

    Instance Attributes:
        - u: an IndustryNode or CompanyNode on one end of this edge
        - v: an IndustryNode or CompanyNode on the other end of this edge
        - weight: the weight of the edge
    """
    u: Node
    v: Node
    weight: float

    def __init__(self, u: Node, v: Node, weight: float) -> None:
        self.u = u
        self.v = v
        self.weight = weight
        # self.v_u_weight = v_u_weight


@check_contracts
class Graph:
    """
    A class representing a graph that will store industry and company nodes

    Instance Attributes:
        - nodes: a dictionary mapping the node name to the node object
    """
    nodes: dict[str, Node]

    def __init__(self) -> None:
        self.nodes = {}

    def add_industry_node(self, name: str, market_cap: float, sentiment: float) -> None:
        """
        Adds an IndustryNode to the graph
        """
        new_node = IndustryNode(name, market_cap, sentiment)
        self.nodes[name] = new_node

    def add_company_node(self, name: str, ticker: str, market_cap: float, industry: str, sentiment: float) -> None:
        """
        Adds an CompanyNode to the graph
        """
        new_node = CompanyNode(name, ticker, market_cap, industry, sentiment)
        self.nodes[name] = new_node

    def add_edge(self, u: str, v: str, u_v_weight, v_u_weight) -> None:
        """
        Add an edge between the two nodes in this graph.

        Raise a ValueError if any of the nodes do not appear in this graph.
        """
        if u in self.nodes and v in self.nodes:
            u_node, v_node = self.nodes[u], self.nodes[v]
            new_edge = Edge(u_node, v_node, u_v_weight, v_u_weight)
            u.edges.add(new_edge)
            v.edges.add(new_edge)
        else:
            raise ValueError

    def get_neighbours_for_node(self, node: Node) -> list[Node]:
        """
        Returns the nodes that are connected with the current node in this graph.

        Raise a ValueError if the node does not appear in this graph.
        """
        return [neighbour for neighbour in node.edges]

    def get_node_by_name(self, name: str) -> Node:
        """
        Return the node with the given name in this graph.

        Raise ValueError if the node with the given name is not in this graph.
        """
        return self.nodes[name]
