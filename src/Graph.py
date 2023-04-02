"""
This Python module contains the node, edge and graph classes to represent our data collected

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and professors
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2023 Mark Zhang, Li Zhang and Luke Zhang
"""
from __future__ import annotations
from python_ta.contracts import check_contracts


from typing import Any


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
    neighbours: set[Node]
    edges: set[Edge]

    def __init__(self, name: str) -> None:
        self.name = name
        self.neighbours = set()
        self.edges = set()

    def get_as_key(self):
        raise NotImplementedError

    def get_pr_score(self):
        score = 0
        for edge in self.edges:
            if edge.u is self:
                score += edge.u_v_weight
            else:
                score += edge.v_u_weight
        return score / len(self.edges)

    def get_ordered_neighbours(self) -> list[Node]:
        """
        Returns a list containing neighbouring nodes to the node given in sorted order according to edge weight

        Not nessecarily a precondition, but this method should be used AFTER the graph has been created, otherwise
        self.neighbours is guaranteed to be empty, thus this method returns an empty array
        """
        connected_stocks = {}
        for edge in node.edges:
            if edge.u is self:
                connected_stocks[edge.v] = edge.u_v_weight
            else:
                connected_stocks[edge.u] = edge.v_u_weight
        return sorted([stock for stock in connected_stocks.keys()],
                      key=lambda stock: connected_stocks[stock], reverse=True)


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
        self.industry = industry
        self.sentiment = sentiment

    def __str__(self) -> str:
        return f'<{self.name}: ticker={self.ticker},sen={self.sentiment},industry={self.industry}>'

    def get_as_key(self):
        return self.ticker


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

    def __str__(self) -> str:
        return f'<{self.name}:cap={self.industry_cap},sen={self.sentiment}>'

    def get_as_key(self):
        return self.name

class Edge:
    """
    A class representing the edge of the graph

    Note that this edge is weighted based on frequency (for CompanyNode to CompanyNode)
    or weighted based on market cap (for IndustryNode to CompanyNode)

    Instance Attributes:
        - u: an IndustryNode or CompanyNode on one end of this edge
        - v: an IndustryNode or CompanyNode on the other end of this edge
        - u_v_weight: the weight of the edge going from node u to node v
        - v_u_weight: the weight of the edge going from node v to node u
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

    def get_average_weight(self):
        return (self.u_v_weight + self.v_u_weight) / 2

    def __str__(self):
        return f'{self.u} - {self.v}'

@check_contracts
class Graph:
    """
    A class representing a graph that will store industry and company nodes

    Instance Attributes:
        - nodes: a dictionary mapping the node name to the node object
    """
    nodes: dict[str, Node]
    edges: set[Edge]

    def __init__(self) -> None:
        self.nodes = {}
        self.edges = set()

    def add_industry_node(self, node: IndustryNode) -> None:
        """
        Adds an IndustryNode to the graph
        """
        self.nodes[node.name] = node

    def add_company_node(self, node: CompanyNode) -> None:
        """
        Adds a CompanyNode to the graph
        """
        self.nodes[node.ticker] = node

    def add_edge(self, u: str, v: str, u_v_weight: float, v_u_weight: float) -> None:
        """
        Add an edge between the two nodes in this graph.

        Raise a ValueError if any of the nodes do not appear in this graph.
        """
        if u in self.nodes and v in self.nodes:
            u_node, v_node = self.nodes[u], self.nodes[v]
            new_edge = Edge(u_node, v_node, u_v_weight, v_u_weight)
            u_node.neighbours.add(v_node)
            v_node.neighbours.add(u_node)
            u_node.edges.add(new_edge)
            v_node.edges.add(new_edge)
            self.edges.add(new_edge)
        else:
            raise ValueError

    def get_node_by_name(self, name: str) -> Node:
        """
        Return the node with the given name in this graph. (Mostly for testing)

        Raise ValueError if the node with the given name is not in this graph.
        """
        return self.nodes[name]

    def remove_edge(self, edge: Edge) -> None:
        """
        Removes edge from the graph
        """
        u, v = edge.u.name, edge.v.name
        self.nodes[u].edges.remove(edge)
        self.nodes[v].edges.remove(edge)
        self.graph.edges.remove(edge)

    def get_best_sentiment_stocks(self) -> list[Node]:
        """
        Returns a list containing nodes in sorted order based on sentiment values
        """
        all_nodes = set(self.graph.nodes.values())
        return sorted([node for node in all_nodes], key=lambda node: node.sentiment, reverse=True)
