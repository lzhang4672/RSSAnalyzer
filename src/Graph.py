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
        - neighbours: nodes connected to self
    """
    name: str
    edges: set[Edge]

    def __init__(self, name: str) -> None:
        self.name = name
        self.edges = set()


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

    Note that this edge is bi-weighted

    Instance Attributes:
        - u: an IndustryNode or CompanyNode on one end of this edge
        - v: an IndustryNode or CompanyNode on the other end of this edge
        - u_v_weight: weight for the edge going from u to v
        - v_u_weight: weight for edge going from v to u
    """
    u: Node
    v: Node
    u_v_weight: float
    v_u_weight: float

    def __init__(self, u: Node, v: Node, u_v_weight: float, v_u_weight: float) -> None:
        self.u = u
        self.v = v
        self.u_v_weight = u_v_weight
        self.v_u_weight = v_u_weight

    def get_weight(self) -> float:
        """
        Returns the average weight of the edge
        """
        return (self.u_v_weight + self.v_u_weight) / 2


@check_contracts
class Graph:
    """
    Abstract class for graph
    """
    nodes: dict[str, Node]

    def __init__(self) -> None:
        self.nodes = {}

    def add_node(self) -> None:
        """
        Adds a node to the graph
        """
        raise NotImplementedError

    def add_node_with_edges(self) -> None:
        """
        Adds a node as well as the edges it has
        """
        raise NotImplementedError

    def add_edge(self, u: Node, v: Node, u_v_weight, v_u_weight) -> None:
        """
        Add an edge between the two nodes in this graph.

        Raise a ValueError if any of the nodes do not appear in this graph.
        """
        if u in self.nodes and v in self.nodes:
            new_edge = Edge(u, v, u_v_weight, v_u_weight)
            u.edges.append(new_edge)
            v.edges.append(new_edge)
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



@check_contracts
class IndustryGraph(Graph):
    """
    Graph where nodes are industries
    """

    @override
    def add_node(self, name: str, market_cap: float, sentiment: float) -> None:
        """
        Adds an IndustryNode to the graph
        """
        new_node = IndustryNode(name, market_cap, sentiment)
        self.nodes[name] = new_node

    def add_edge(self, u: Node, v: Node, u_v_weight: float, v_u_weight: float) -> None:
        """
        Adds an edge between two nodes in the graph
        """
        super.add_edge(u, v, u_v_weight, v_u_weight)

    def get_neighbours_for_node(self, node: Node) -> list[Node]:
        """
        Returns the nodes that are connected with the current node in this graph.
        """
        return super().get_neighbours_for_node(node)

    def get_node_by_name(self, name: str) -> Node:
        """
        Returns the node with the given name in the graph
        """
        return super().get_node_by_name(name)

class CompanyGraph(Graph):
    """
    Graph where the nodes are companies
    """
    @override
    def add_node(self, ticker: str, market_cap: float, industry: str, sentiment: float) -> None:
        """
        Adds an CompanyNode to the graph
        """
        new_node = CompanyNode(ticker, market_cap, industry, sentiment)
        self.nodes[name] = new_node

    def add_edge(self, u: Node, v: Node, u_v_weight: float, v_u_weight: float) -> None:
        """
        Adds an edge to the graph
        """
        super.add_edge(u, v, u_v_weight, v_u_weight)

    def get_neighbours_for_node(self, node: Node) -> list[Node]:
        """
        Returns the nodes that are connected with the current node in this graph.
        """
        return super.get_neighbours_for_node(node)

    def get_node_by_name(self, name: str) -> Node:
        """
        Returns the node with the given name in the graph
        """
        return super.get_node_by_name(name)
