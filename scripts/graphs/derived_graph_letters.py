import networkx as nx
from matplotlib import pyplot as plt
from pathlib import Path
import os

from mmm.pianorolls.graphs import Graph

# Path
figures_path = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('graphs')
name = str(os.path.basename(__file__))[:-3]

# Graph
graph = Graph()

# Lists
list_1 = ['$S$', '$A$', '$B$', '$C$', '$D$', '$A$', '$A$', '$E$']

# Add nodes
graph.add_node(1, pos=(0, 0), label=list_1[0])
graph.add_node(2, pos=(1, 1), label=list_1[1])
graph.add_node(3, pos=(1, -1), label=list_1[2])
graph.add_node(4, pos=(2, 1), label=list_1[3])
graph.add_node(5, pos=(2, -1), label=list_1[4])
graph.add_node(6, pos=(3, 0), label=list_1[5])
graph.add_node(7, pos=(4, 0), label=list_1[6])
graph.add_node(8, pos=(5, 0), label=list_1[7])

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
nx.draw_networkx_labels(graph, pos, nx.get_node_attributes(graph, 'label'))
nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'weight'))

plt.axis('off')
plt.tight_layout()

file_path = figures_path / (name + '_0.pdf')
plt.savefig(file_path)

plt.show()
