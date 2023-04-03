from python_ta.contracts import check_contracts
from Graph import CompanyNode, IndustryNode, Edge, Graph



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
class GraphVisualizer:
    """A class responsible for displaying the graph visualization of a graph object


    Instance Attributes:
    -








     """
    @check_contracts
    def __init__(self):


