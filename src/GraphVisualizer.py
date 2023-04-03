from python_ta.contracts import check_contracts
from StockGraphAnalyzer import StockGraphAnalyzer
from Graph import CompanyNode, IndustryNode, Edge, Graph
from dataclasses import dataclass
from pyvis.network import Network
from StockInfo import get_stock_sentiment_as_text
import webbrowser
import os

# path to store graphs
GRAPHS_STORAGE = '/graphs/'

# physics settings for the graph
JSON_OPTIONS = """"
const options = {
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -10,
      "springLength": 400,
      "springConstant": 0.1,
      "damping": 1
    },
    "minVelocity": 0.01,
    "maxVelocity": 100,
    "solver": "forceAtlas2Based"
  }
}
"""
# dictionary containing industry to color values
INDUSTRY_COLORS = {
    'Financial Services': '#a7bac4',
    'Pharmacy and Health Care': '#a485c9',
    'Consumer Goods': '#c9be85',
    'E-commerce': '#c99d85',
    'Medical Equipment': '#c985b7',
    'Software': '#7aa2ff',
    'Metals and Mining': '#d1c890',
    'Technology': '#d7d9db',
    'Banking': '#96d9ac',
    'Automotive': '#51b8fc',
    'Semiconductors': '#515cfc',
    'Energy and Utilities': '#dcff17',
    'Oil and Gas': '#898a86',
    'Real Estate': '#d1a64f',
    'Media and Entertainment': '#ffa3ce',
    'Transportation': '#c5dbd6',
    'Manufacturing': '#79588a',
    'Ride-hailing/Food-delivery': '#43bdbf',
    'Retail': '#5c4ff0',
    'Financial Technology': '#9e374c',
    'Telecommunications': '#fa48d3',
    'Default': '#7e9ebf'
}


# Data Classes
@dataclass
class NodeVisualizer:
    """A data class that stores the information for visualizing a node

    Instance Attributes:
        - color: a hex color string that represents the color of the node
        - id: a unique string that represents the id of the node
        - label: a string representing the text displayed under the node
        - value: a number used for scaling purposes
        - title: a string that is displayed when the node is hovered

    Representation Invariants:
        - self.id is unique in all NodeVisualizer objects
        - self.label != ''
        - self.value > 0
        - self.color is a valid hex color string

    """
    color: str
    id: str
    label: str
    title: str
    value: float


@dataclass
class EdgeVisualizer:
    """A data class that stores the information for visualizing an edge

     Instance Attributes:
        - from_node_visualizer: a NodeVisualizer object representing one end of the edge
        - to_node_visualizer: a NodeVisualizer object representing the other end of the edge
        - value: a number used for scaling purposes
        - title: a string that is displayed when the edge is hovered on
        - color: a string representing the hex color of the edge

    Representation Invariants:
        - self.value > 0
        - self.color is a valid hex color string
    """
    from_node_visualizer: NodeVisualizer
    to_node_visualizer: NodeVisualizer
    value: float
    title: str
    color: str


# top level functions
# @check_contracts
def get_industry_color(industry: str) -> str:
    """Returns the color associated with the industry, if no matches is found, a default color is returned
    """
    if industry in INDUSTRY_COLORS:
        return INDUSTRY_COLORS[industry]
    return INDUSTRY_COLORS['Default']


# @check_contracts
def get_significant_neighbours_text(node: CompanyNode | IndustryNode) -> str:
    """Returns a string that displays significant neighbours to the node"""
    n_neighbours = 3
    text = ""
    if type(node) == IndustryNode:
        # the node is an industry node so display more neighbours
        n_neighbours = 5
        text += "[Leading Companies]\n"
    else:
        text += "[Related Entities]\n"
    significant_neighbours = node.get_ordered_neighbours()
    n_neighbours = min(len(significant_neighbours), n_neighbours)
    for i in range(n_neighbours):
        neighbour = significant_neighbours[i]
        text += str(i + 1) + ". " + neighbour.name + "\n"
    return text


def get_ranking_sentiment_neighbours_text(node: CompanyNode | IndustryNode) -> str:
    """Returns a string that displays highest and lowest sentiment neighbours to the node"""
    n_neighbours = 3
    text = ""
    if type(node) == IndustryNode:
        # the node is an industry node so display more neighbours
        n_neighbours = 5
    text += "[Lowest Connected Sentiment Entities]\n"
    # get lowest sentiment companies
    ordered_sentiment_neighbours = node.get_ordered_sentiment_neighbours()
    n_neighbours = min(len(ordered_sentiment_neighbours), n_neighbours)
    for i in range(n_neighbours):
        neighbour = ordered_sentiment_neighbours[i]
        text += str(i + 1) + ". " + neighbour.name + "\n"
    text += "[Highest Connected Sentiment Entities]\n"
    # get highest sentiment companies
    ordered_sentiment_neighbours.reverse()
    for i in range(n_neighbours):
        neighbour = ordered_sentiment_neighbours[i]
        text += str(i + 1) + ". " + neighbour.name + "\n"
    return text

# @check_contracts
def get_node_visualization_title(node: CompanyNode | IndustryNode, analyzer: StockGraphAnalyzer) -> str:
    """Returns a string storing the information that should be displayed when a node is hovered upon
    """
    if type(node) == CompanyNode:
        # the node is a company node
        # add market cap info
        ret = ""
        ret += "===[BASIC INFO]===\n"
        ret += node.name + " (" + node.ticker + ")\n" + "[Market Cap]\n" + str(node.market_cap) + "Billion Dollars (" \
                                                                                                  "USD)\n "
        # add connected companies info
        ret += "[Number Of Connected Companies]\n" + str(len(node.neighbours)) + "\n" \
               + get_significant_neighbours_text(node)
        # add industry info
        ret += "[Industry]\n" + node.industry + "\n" \
            # add sentiment info
        ret += "===[ANALYSIS INFO]===\n"
        sentiment_rank_index = analyzer.ordered_node_sentiment_scores.index(node.ticker)
        ret += "[Sentiment]\n" + get_stock_sentiment_as_text(node.sentiment) + " (" + str(node.sentiment) + ")\n"
        ret += "Rank: " + str(sentiment_rank_index + 1) + "\n"
        ret += get_ranking_sentiment_neighbours_text(node)
        # add page ranking info
        ret += "===[ADDITIONAL INFO]===\n"
        page_rank_index = analyzer.ordered_pagerank_scores.index(node.ticker)
        ret += "[NodeRank]\n" + "Rank: " + str(page_rank_index + 1) + "\n" + "Score: " + str(node.get_pr_score()) + "\n"
    else:
        # the node is an industry node
        ret = "[Combined Market Cap]\n" + str(node.industry_cap) + " Billion Dollars (USD)\n" \
              + "[Overall Sentiment]\n" + get_stock_sentiment_as_text(node.sentiment) + " (" \
              + str(node.sentiment) + ")\n" + "[Number Of Companies]\n" + \
              str(len(node.neighbours)) + "\n" + get_significant_neighbours_text(node) \
                + get_ranking_sentiment_neighbours_text(node)

    return ret


# @check_contracts
def get_edge_visualization_title(edge: Edge) -> str:
    """Returns a string storing the information that should be displayed when an edge is hovered upon
    """
    u_node = edge.u
    v_node = edge.v
    if type(u_node) == type(v_node) == CompanyNode:
        # both nodes are company nodes
        return "[Connection Frequency]\n" + u_node.name + "->" + v_node.name + ": " + str(edge.u_v_weight) \
               + "\n" + v_node.name + "->" + u_node.name + ": " + str(edge.v_u_weight) + "\n"
    else:
        industry_node, company_node, weighting, connection = None, None, 0, ''
        if type(v_node) == IndustryNode:
            # v node is the industry node
            industry_node = v_node
            company_node = u_node
            weighting = edge.v_u_weigh
        else:
            # u is the industry node
            industry_node = u_node
            company_node = v_node
            weighting = edge.u_v_weight
        return "[Connection Influence]\n" + industry_node.name + "->" + company_node.name + ": " + str(weighting)


# @check_contracts
class GraphVisualizer:
    """A class responsible for displaying the graph visualization of a graph object using pyvis


    Instance Attributes:
        - graph: a Graph object representing the graph to be visualized
        - analyzer: a StockGraphAnalyzer object storing the analzed data of the graph
        - network: a pyvis network object that is used to build the visualized graph
    Private Instance Attributes:
        - _visualized_nodes: a dictionary where the key is a Node which corresponds to its NodeVisualizer object
        - _visualized_edges: a list of all the EdgeVisualizer objects
        - _id: a string that represents the save file

     """
    graph: Graph
    analyzer: StockGraphAnalyzer
    _visualized_nodes: dict[CompanyNode | IndustryNode, NodeVisualizer] = {}
    _visualized_edges: list[EdgeVisualizer] = []
    _id: str

    # @check_contracts
    def _add_visualize_node(self, node: CompanyNode | IndustryNode) -> None:
        """Adds a node to be visualized"""
        if node not in self._visualized_nodes:
            title, node_id = get_node_visualization_title(node, self.analyzer), node.name
            # the node is not added yet
            if type(node) == CompanyNode:
                # the node is a company node
                label = node.name + " (" + node.ticker + ")"
                color = get_industry_color(node.industry)
                value = node.market_cap
            else:
                # the node is an industry node
                label = node.name + " Industry"
                color = get_industry_color(node.name)
                value = node.industry_cap
            self._visualized_nodes[node] = \
                NodeVisualizer(label=label, title=title, color=color, id=node_id, value=value)

    def _add_visualize_edge(self, edge: Edge) -> None:
        """Adds an edge to be visualized
        """
        u_node = edge.u
        v_node = edge.v
        self._add_visualize_node(v_node)
        self._add_visualize_node(u_node)
        if type(u_node) == type(v_node) == CompanyNode:
            # the node are company nodes
            color = get_industry_color(u_node.industry)
            if u_node.industry != v_node.industry:
                # if they aren't in the same industry, use the default edge color
                color = get_industry_color('Default')
            value = edge.get_average_weight()
            title = get_edge_visualization_title(edge)
            self._visualized_edges += [EdgeVisualizer(
                from_node_visualizer=self._visualized_nodes[u_node],
                to_node_visualizer=self._visualized_nodes[v_node],
                color=color,
                value=value,
                title=title
            )]
        else:
            # one of the nodes is the industry node
            company_node, industry_node = None, None
            if type(u_node) == CompanyNode:
                # the u_node is the company node
                company_node = u_node
                industry_node = v_node
                weight = edge.v_u_weight
            else:
                # the v_node is the company node
                company_node = v_node
                industry_node = u_node
                weight = edge.u_v_weight
            self._visualized_edges += [EdgeVisualizer(
                from_node_visualizer=self._visualized_nodes[industry_node],
                to_node_visualizer=self._visualized_nodes[company_node],
                color=get_industry_color(industry_node.name),
                value=weight,
                title=get_edge_visualization_title(edge)
            )]

    def show_graph(self) -> None:
        """When called, the object will open the graph through the browser"""
        saved_file_name = GRAPHS_STORAGE + self._id + "_graph.html"
        if os.path.exists('.' + saved_file_name):
            # the file exists so open the saved html file in the browser
            webbrowser.open_new_tab('file:///' + os.getcwd() + saved_file_name)

    # @check_contracts
    def _build_visualization(self) -> None:
        """Builds up the visualization objects and creates the html file that contains the visualization of the graph"""
        # add the nodes
        for node_name in self.graph.nodes:
            node = self.graph.nodes[node_name]
            self._add_visualize_node(node)
        # add the edges
        for edge in self.graph.edges:
            self._add_visualize_edge(edge)
        # add relavant information to the network
        # render nodes
        for node in self._visualized_nodes:
            node_visualization_data = self._visualized_nodes[node]
            self.network.add_node(
                node_visualization_data.id,
                label=node_visualization_data.label,
                value=node_visualization_data.value,
                title=node_visualization_data.title,
                color=node_visualization_data.color
            )
        # render edges
        for edge_visualization_data in self._visualized_edges:
            self.network.add_edge(
                edge_visualization_data.from_node_visualizer.id,
                edge_visualization_data.to_node_visualizer.id,
                title=edge_visualization_data.title,
                value=edge_visualization_data.value,
                color=edge_visualization_data.color
            )
        # create html page
        self.network.show('.' + GRAPHS_STORAGE + self._id + "_graph.html")

    # @check_contracts
    def __init__(self, graph_id: str, stock_graph_analyzer: StockGraphAnalyzer):
        """Intializes a GraphVisualizer object"""
        # intialize all attributes
        self.analyzer = stock_graph_analyzer
        self.graph = stock_graph_analyzer.graph
        self._id = graph_id
        # only include the filter menu if the dataset is small enough
        include_select_menu = len(self.graph.nodes) <= 50
        self.network = Network(height="1050px", width="100%", bgcolor="#292d33", font_color='white',
                               select_menu=include_select_menu)
        self.network.set_options(JSON_OPTIONS)
        # build the visualization
        self._build_visualization()
