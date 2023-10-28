import networkx as nx
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# Parse the GraphML data
tree = ET.parse('./map2check/witness.graphml')
root = tree.getroot()

# Create an empty graph
graph = nx.DiGraph()

# Iterate over nodes and add them to the graph
for node in root.findall('.//{http://graphml.graphdrawing.org/xmlns}node'):
    node_id = node.get('id')
    graph.add_node(node_id)

# Iterate over edges and add them to the graph
for edge in root.findall('.//{http://graphml.graphdrawing.org/xmlns}edge'):
    source = edge.get('source')
    target = edge.get('target')
    graph.add_edge(source, target)

# Visualize the graph
nx.draw(graph, with_labels=True)
plt.show()
