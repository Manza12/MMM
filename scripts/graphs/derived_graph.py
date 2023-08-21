import networkx as nx
from matplotlib import pyplot as plt
from pathlib import Path
import os

from mmm.pianorolls.graphs import Graph

# Path
folder = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('graphs')
folder.mkdir(parents=True, exist_ok=True)
name = str(os.path.basename(__file__))[:-3]

# Graph
graph = Graph()

# Lists
list_1 = [1, 2, 3, 4, 5, 6, 7, 8]
list_2 = ['$S$', '$A$', '$B$', '$C$', '$D$', '$D$', '$A$', '$E$']

# Add nodes
graph.add_node(1, pos=(0, 0), label='$%s$' % list_1[0])
graph.add_node(2, pos=(1, 1), label='$%s$' % list_1[1])
graph.add_node(3, pos=(1, -1), label='$%s$' % list_1[2])
graph.add_node(4, pos=(2, 1), label='$%s$' % list_1[3])
graph.add_node(5, pos=(2, -1), label='$%s$' % list_1[4])
graph.add_node(6, pos=(3, 0), label='$%s$' % list_1[5])
graph.add_node(7, pos=(4, 0), label='$%s$' % list_1[6])
graph.add_node(8, pos=(5, 0), label='$%s$' % list_1[7])

# Add edges
graph.add_edge(1, 2)
graph.add_edge(1, 3)
graph.add_edge(2, 4)
graph.add_edge(2, 5)
graph.add_edge(3, 4)
graph.add_edge(3, 5)
graph.add_edge(4, 6)
graph.add_edge(5, 6)
graph.add_edge(6, 7)
graph.add_edge(7, 8)

# Plot graph
plt.figure(figsize=(5., 2.))

pos = nx.get_node_attributes(graph, 'pos')
nx.draw_networkx_edges(graph, pos, arrows=True)
nx.draw_networkx_labels(graph, pos, nx.get_node_attributes(graph, 'label'), font_size=14)
nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'))

plt.axis('off')
plt.tight_layout()

file_path = folder / (name + '_0.pdf')
plt.savefig(file_path)

# Plot first derivative graph
graph_1 = graph.derive(placement=0.3)

plt.figure(figsize=(5., 2.))

pos = nx.get_node_attributes(graph_1, 'pos')
nx.draw_networkx_edges(graph_1, pos, arrows=True, node_size=1200)
nx.draw_networkx_labels(graph_1, pos, nx.get_node_attributes(graph_1, 'label'), font_size=14)
nx.draw_networkx_edge_labels(graph_1, pos, edge_labels=nx.get_edge_attributes(graph_1, 'weight'))

plt.axis('off')
plt.tight_layout()

file_path = folder / (name + '_1.pdf')
plt.savefig(file_path)

# Plot second derivative graph
graph_2 = graph_1.derive(placement=0.6)

plt.figure(figsize=(6., 2.))

pos = nx.get_node_attributes(graph_2, 'pos')
nx.draw_networkx_edges(graph_2, pos, arrows=True, node_size=2500)
nx.draw_networkx_labels(graph_2, pos, nx.get_node_attributes(graph_2, 'label'), font_size=14)
nx.draw_networkx_edge_labels(graph_2, pos, edge_labels=nx.get_edge_attributes(graph_2, 'weight'))

plt.axis('off')
plt.tight_layout()

file_path = folder / (name + '_2.pdf')
plt.savefig(file_path)

plt.show()
