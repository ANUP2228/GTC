import networkx as nx
import matplotlib.pyplot as plt

adj_a = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0]
]

adj_b = [
    [0, 1, 0, 0, 0, 0, 0, 1], 
    [1, 0, 1, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 0], 
    [1, 1, 1, 0, 1, 1, 0, 0], 
    [0, 0, 0, 1, 0, 1, 0, 0], 
    [0, 0, 0, 1, 1, 0, 1, 1], 
    [0, 0, 0, 0, 0, 1, 0, 1], 
    [1, 1, 0, 0, 0, 1, 1, 0]  
]

def build_graph(matrix):
    G = nx.Graph()
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            for _ in range(matrix[i][j]):
                G.add_edge(i, j)
    return G

pos_a = {0: (-1, 1), 1: (1, 1), 2: (1, -1), 3: (-1, -1)}
labels_a = {i: chr(65 + i) for i in range(4)} # A, B, C, D

pos_b = {
    0: (-1, 1),  2: (1, 1),   4: (1, -1),  6: (-1, -1),
    7: (-1, 0),  1: (0, 1),   3: (1, 0),   5: (0, -1)   
}
labels_b = {i: chr(65 + i) for i in range(8)}


def has_euler_circuit(G):
    return nx.is_connected(G) and all(d % 2 == 0 for _, d in G.degree())

def find_euler_circuit(G):
    if not has_euler_circuit(G): return None
    return list(nx.eulerian_circuit(G))


G1 = build_graph(adj_a)
G2 = build_graph(adj_b)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, G, pos, lbls, title in zip(axes, [G1, G2], [pos_a, pos_b], [labels_a, labels_b], ["Graph (a)", "Graph (b)"]):
    nx.draw(G, pos, ax=ax, with_labels=True, labels=lbls, node_color="white", 
            edgecolors="black", node_size=1000, width=2, font_weight='bold')
    
    circuit = find_euler_circuit(G)
    if circuit:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=circuit, edge_color="red", width=4, alpha=0.5)
        ax.set_title(f"{title}: Euler Circuit Found", color="green")
    else:
        ax.set_title(f"{title}: No Euler Circuit", color="red")

plt.tight_layout()
plt.show()