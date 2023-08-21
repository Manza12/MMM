import os
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

mpl.rcParams['mathtext.fontset'] = 'cm'

graph = nx.DiGraph()

# Nodes
graph.add_node('v_1^1', pos=(0, 0), label=r'$v_1^1$')

graph.add_node('v_1^2', pos=(1, -1), label=r'$v_1^2$')
graph.add_node('v_2^2', pos=(1, 0), label=r'$v_2^2$')
graph.add_node('v_3^2', pos=(1, 1), label=r'$v_3^2$')

graph.add_node('v_1^3', pos=(2, -0.5), label=r'$v_1^3$')
graph.add_node('v_2^3', pos=(2, 0.5), label=r'$v_2^3$')

graph.add_node('v_1^4', pos=(3, -1.5), label=r'$v_1^4$')
graph.add_node('v_2^4', pos=(3, -0.5), label=r'$v_2^4$')
graph.add_node('v_3^4', pos=(3, 0.5), label=r'$v_3^4$')
graph.add_node('v_4^4', pos=(3, 1.5), label=r'$v_4^4$')

graph.add_node('v_1^5', pos=(4, -0.5), label=r'$v_1^5$')
graph.add_node('v_2^5', pos=(4, 0.5), label=r'$v_2^5$')

graph.add_node('v_1^6', pos=(5, 0), label=r'$v_1^6$')

# Edges
graph.add_edge('v_1^1', 'v_1^2')
graph.add_edge('v_1^1', 'v_2^2')
graph.add_edge('v_1^1', 'v_3^2')

graph.add_edge('v_1^2', 'v_1^3')
graph.add_edge('v_1^2', 'v_2^3')
graph.add_edge('v_2^2', 'v_1^3')
graph.add_edge('v_2^2', 'v_2^3')
graph.add_edge('v_3^2', 'v_1^3')
graph.add_edge('v_3^2', 'v_2^3')

graph.add_edge('v_1^3', 'v_1^4')
graph.add_edge('v_1^3', 'v_2^4')
graph.add_edge('v_1^3', 'v_3^4')
graph.add_edge('v_1^3', 'v_4^4')
graph.add_edge('v_2^3', 'v_1^4')
graph.add_edge('v_2^3', 'v_2^4')
graph.add_edge('v_2^3', 'v_3^4')
graph.add_edge('v_2^3', 'v_4^4')

graph.add_edge('v_1^4', 'v_1^5')
graph.add_edge('v_1^4', 'v_2^5')
graph.add_edge('v_2^4', 'v_1^5')
graph.add_edge('v_2^4', 'v_2^5')
graph.add_edge('v_3^4', 'v_1^5')
graph.add_edge('v_3^4', 'v_2^5')
graph.add_edge('v_4^4', 'v_1^5')
graph.add_edge('v_4^4', 'v_2^5')

graph.add_edge('v_1^5', 'v_1^6')
graph.add_edge('v_2^5', 'v_1^6')

# Plot
fig = plt.figure(figsize=(8., 4.))

pos = nx.get_node_attributes(graph, 'pos')
labels = nx.get_node_attributes(graph, 'label')

nx.draw_networkx_labels(graph, pos, labels=labels, font_size=16)
nx.draw_networkx_edges(graph, pos, edge_color='k', arrows=True, node_size=700)

plt.axis('off')
plt.tight_layout()

# Path
figures_path = Path('..') / Path('..') / Path('phd') / Path('chapter_5') / Path('graphs')
name = str(os.path.basename(__file__))[:-3]

# Save
plt.savefig(figures_path / Path(name + '.pdf'))

plt.show()
