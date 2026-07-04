import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = [
    (1,2), (1,3), (2,3), (1,4), (2,5),
    (3,4), (3,5), (1,6), (2,6), (4,7), 
    (5,8), (7,8), (7,9), (8,9), (6,9)
]
G.add_edges_from(edges)

pos = {
    1: (-1, 2), 2: (1, 2), 3: (0, 1.5),
    4: (-1.6, 0.5), 5: (1.6, 0.5), 6: (0, 0),
    7: (-1, -2), 8: (1, -2), 9: (0, -3)
}

plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
plt.title("Original Graph")

S = G.copy()
edges_to_remove = [(1, 3), (2, 3), (7, 8), (6, 9)]
S.remove_edges_from(edges_to_remove)

plt.subplot(2, 2, 2)
nx.draw(S, pos, with_labels=True, node_color='lightgreen')
plt.title("Spanning Subgraph\n(Removed specific edges)")

I = G.copy()
nodes_to_keep = {1, 2, 3, 4, 5}
nodes_to_remove = [n for n in I.nodes() if n not in nodes_to_keep]
I.remove_nodes_from(nodes_to_remove)

plt.subplot(2, 2, 3)
nx.draw(I, pos, with_labels=True, node_color='salmon')
plt.title("Induced Subgraph [1,2,3,4,5]\n(Removed nodes 6,7,8,9)")

E = G.copy()
keep_edges = {(1, 2), (2, 5), (5, 8), (8, 9)}
edges_to_remove = [e for e in E.edges() if e not in keep_edges and e[::-1] not in keep_edges]
E.remove_edges_from(edges_to_remove)

plt.subplot(2, 2, 4)
nx.draw(E, pos, with_labels=True, node_color='khaki')
plt.title("Edge Subgraph [(1,2), (2,5), (5,8), (8,9)]\n(Removed all other edges)")

plt.tight_layout()
plt.show()