import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
def print_adjacency_matrix(G, name):
    print(f"\nAdjacency Matrix of {name}:")
    nodes = list(G.nodes())
    A = nx.to_numpy_array(G, nodelist=nodes, dtype=int)
    print("   ", nodes)
    for i, row in enumerate(A):
        print(nodes[i], row.astype(int))
def manual_isomorphic_check(G1, G2):
    """
    Manually checks if G1 and G2 are isomorphic using backtracking.
    Returns (True, mapping) if isomorphic, else (False, None).
    """
    nodes1 = list(G1.nodes())
    nodes2 = list(G2.nodes())

    if len(nodes1) != len(nodes2): return False, None
    if sorted([d for n, d in G1.degree()]) != sorted([d for n, d in G2.degree()]):
        return False, None

    mapping = {}
    used_in_G2 = set()

    def is_consistent(u, v):
        for neighbor in G1.neighbors(u):
            if neighbor in mapping:
                if not G2.has_edge(v, mapping[neighbor]):
                    return False
        
        for neighbor_v in G2.neighbors(v):
            mapped_back = next((k for k, val in mapping.items() if val == neighbor_v), None)
            if mapped_back is not None and not G1.has_edge(u, mapped_back):
                return False
        return True

    def backtrack(index):
        if index == len(nodes1):
            return True

        u = nodes1[index]
        for v in nodes2:
            if v not in used_in_G2:
                if is_consistent(u, v):
                    mapping[u] = v
                    used_in_G2.add(v)
                    if backtrack(index + 1):
                        return True
                    used_in_G2.remove(v)
                    del mapping[u]
        return False

    if backtrack(0):
        return True, mapping
    return False, None

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
    1: (-1, 2), 2: (0, 1.5), 3: (1, 2), 4: (1, 1),
    5: (2, 1), 6: (1.5, 0), 7: (2, -1), 8: (1, -1),
    9: (1, -2), 10: (0, -1.5), 11: (-1, -2), 12: (-1, -1),
    13: (-2, -1), 14: (-1.5, 0), 15: (-2, 1), 16: (-1, 1)
}

pos3 = {}
for i in range(1, 17):
    angle = np.deg2rad(90 - (i-1) * 360/16)
    pos3[i] = (2 * np.cos(angle), 2 * np.sin(angle))
print("\nGraph G1 Degrees:", dict(G1.degree()))
print_adjacency_matrix(G1, "G1")

pairs = [("G1", "G2", G1, G2), ("G2", "G3", G2, G3), ("G1", "G3", G1, G3)]

print("Manual Isomorphism Results:")
print("-" * 30)

for name1, name2, graph1, graph2 in pairs:
    is_iso, mapping = manual_isomorphic_check(graph1, graph2)
    print(f"{name1} ≅ {name2}: {is_iso}")
    if is_iso:
        print(f"Mapping: {mapping}")
    print("-" * 30)

plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
nx.draw(G1, pos1, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold')
plt.title("G1 (Octagon-Star)")


plt.subplot(1, 3, 3)
nx.draw(G3, pos3, with_labels=True, node_color='wheat', node_size=500, font_weight='bold')
plt.title("G3 (16-Node Ring)")

plt.subplot(1, 3, 2)
ax = plt.gca()
# Draw edges first so nodes/labels appear on top
# Use curved arrows for the requested G2 edges and straight lines for all others
curved_rads = {
    tuple(sorted((5, 15))): 0.9,
    tuple(sorted((1, 11))): 0.6,
    tuple(sorted((3, 9))): -0.6,
    tuple(sorted((7, 13))): -0.9,
}
for (u, v) in G2.edges():
    rad = curved_rads.get(tuple(sorted((u, v))), 0.0)
    patch = FancyArrowPatch(pos2[u], pos2[v], connectionstyle=f"arc3,rad={rad}", arrowstyle='-', color='gray', linewidth=1.2)
    patch.set_zorder(1)
    ax.add_patch(patch)

# Draw nodes and labels on top; set z-order on returned artists
nodes_coll = nx.draw_networkx_nodes(G2, pos2, node_color='lightgreen', node_size=500)
nodes_coll.set_zorder(2)
label_artists = nx.draw_networkx_labels(G2, pos2, font_weight='bold')
for text in label_artists.values():
    text.set_zorder(3)
plt.title("G2 (Clover Cross)")
plt.axis('off')
plt.show()
