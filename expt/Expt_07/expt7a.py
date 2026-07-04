import networkx as nx
import matplotlib.pyplot as plt
G=nx.Graph()
edges = [
    ('A', 'B', 4),
    ('A', 'C', 6),
    ('A', 'D', 5),
    ('B', 'C', 1),
    ('B', 'E', 7),
    ('C', 'D', 2),
    ('C', 'F', 4),
    ('C', 'E', 5),
    ('D', 'F', 5),
    ('E', 'F', 1),
    ('E', 'G', 6),
    ('F', 'G', 8)
]
G.add_weighted_edges_from(edges)
pos = {
    'A': (-1, 1),
    'B': (0, 2),
    'C': (0, 1),
    'D': (0, 0),
    'E': (1, 1.5),
    'F': (1, 0.5),
    'G': (2, 1)
}
source = 'A'
target = 'G'
path = nx.dijkstra_path(G, source, target)
distance = nx.dijkstra_path_length(G, source, target)
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
nx.draw(G, pos, with_labels=True, node_size=800)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Original Graph")
plt.subplot(1,2,2)
nx.draw(G, pos, with_labels=True, node_size=800, alpha=0.3)
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title(f"Shortest Path\n{path} | Cost = {distance}")
plt.tight_layout()
plt.show()