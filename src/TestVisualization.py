import webbrowser
import os
from pyvis.network import Network

net = Network()

net.add_node('A', label='Alex')
net.add_node('B', label='Cathy')

net.show('graphs/nodes.html')
net.show_buttons(filter_='Physics')
webbrowser.open_new_tab('file:///'+os.getcwd()+'/graphs/nodes.html')
