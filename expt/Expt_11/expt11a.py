import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

edges = [
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 6),
    (2, 3),
    (2, 5),
    (2, 6),
    (3, 4),
    (3, 5),
    (4, 7),
    (5, 8),
    (6, 9),
    (7, 8),
    (7, 9),
    (8, 9),
]

G.add_edges_from(edges)

coloring = nx.coloring.greedy_color(G, strategy="largest_first")

print("Vertex Colors:")
for node, color in coloring.items():
    print(f"Vertex {node} ---> Color {color}")

color_map = []

colors = [
    "red",
    "blue",
    "green",
    "yellow",
    
]

for node in G.nodes():
    color_map.append(colors[coloring[node]])

pos = {
   1: (-1, 2), 2: (1, 2), 3: (0, 1.5),
    4: (-1.6, 0.5), 5: (1.6, 0.5), 6: (0, 0),
    7: (-1, -2), 8: (1, -2), 9: (0, -3)
}

plt.figure(figsize=(8, 6))

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=color_map,
    node_size=1200,
    font_size=12
)

plt.title("Graph Coloring")
plt.show()