import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def print_adjacency_matrix(G, name):
    print(f"\nAdjacency Matrix of {name}:")
    nodes = list(G.nodes())
    A = nx.to_numpy_array(G, nodelist=nodes, dtype=int)
    print("   ", nodes)
    for i, row in enumerate(A):
        print(nodes[i], row.astype(int))

G1 = nx.Graph()
G1.add_nodes_from(range(1, 17))
G1.add_edges_from([
    (1,2),(1,8),(1,9), (2,3),(2,10), (3,4),(3,11), (4,5),(4,12),
    (5,6),(5,13), (6,7),(6,14), (7,8),(7,15), (8,16), (9,12),
    (12,15),(15,10), (10,13),(13,16), (16,11),(11,14),(14,9)
])

G2 = nx.Graph()
G2.add_nodes_from(range(1, 17))
G2.add_edges_from([
    (1,2),(1,11),(1,16), (2,3),(2,10),(3,4), (3,9),(4,5),(4,12),
    (5,6),(5,15),(6,7), (6,14),(7,8),(7,13), (8,9),(8,16),(9,10),
    (10,11),(11,12),(12,13), (13,14),(14,15),(15,16)
])

G3 = nx.Graph()
G3.add_nodes_from(range(1, 17))
G3.add_edges_from([
    (1,2),(2,3),(3,4), (4,5),(5,6),(6,7), (7,8),(8,9),(9,10),
    (10,11),(11,12),(12,13), (13,14),(14,15),(15,16), (16,1),
    (1,12),(2,7), (3,14),(4,9),(5,16), (6,11),(8,13),(10,15)
])

pos1 = {}
for i in range(1, 9): 
    angle = np.deg2rad(90 - (i-1) * 360/8)
    pos1[i] = (2 * np.cos(angle), 2 * np.sin(angle))
for i in range(9, 17): 
    angle = np.deg2rad(90 - (i-9) * 360/8)
    pos1[i] = (1 * np.cos(angle), 1 * np.sin(angle))

pos2 = {
    1: (0, 2), 2: (0.7, 1.3), 3: (2, 1), 4: (1.3, 0),
    5: (2, -1), 6: (0.7, -1.3), 7: (0, -2), 8: (-0.7, -1.3),
    9: (-2, -1), 10: (-1.3, 0), 11: (-2, 1), 12: (-0.7, 1.3),
    13: (0.5, 0.5), 14: (0.5, -0.5), 15: (-0.5, -0.5), 16: (-0.5, 0.5)
}

pos3 = {}
for i in range(1, 17):
    angle = np.deg2rad(90 - (i-1) * 360/16)
    pos3[i] = (2 * np.cos(angle), 2 * np.sin(angle))

print("\nGraph G1 Degrees:", dict(G1.degree()))
print_adjacency_matrix(G1, "G1")

iso12 = nx.is_isomorphic(G1, G2)
iso23 = nx.is_isomorphic(G2, G3)
iso13 = nx.is_isomorphic(G1, G3)

print(f"\nG1 ≅ G2: {iso12}")
print(f"G2 ≅ G3: {iso23}")
print(f"G1 ≅ G3: {iso13}")

mapping12 = None
mapping23 = None
mapping13 = None

if iso12:
    mapping12 = nx.isomorphism.vf2pp_isomorphism(G1, G2)
if iso23:
    mapping23 = nx.isomorphism.vf2pp_isomorphism(G2, G3)
if iso13:
    mapping13 = nx.isomorphism.vf2pp_isomorphism(G1, G3)

print("\nMappings:")
if mapping12:
    print("G1 → G2:", mapping12)
if mapping23:
    print("G2 → G3:", mapping23)
if mapping13:
    print("G1 → G3:", mapping13)

plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
nx.draw(G1, pos1, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold')
plt.title("G1 (Octagon-Star)")

plt.subplot(1, 3, 2)
nx.draw(G2, pos2, with_labels=True, node_color='lightgreen', node_size=500, font_weight='bold')
plt.title("G2 (Clover Cross)")

plt.subplot(1, 3, 3)
nx.draw(G3, pos3, with_labels=True, node_color='wheat', node_size=500, font_weight='bold')
plt.title("G3 (16-Node Ring)")

plt.tight_layout()
plt.show()