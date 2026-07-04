import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
print("=" * 60)
print("LINE GRAPH CONSTRUCTION")
print("=" * 60)
n = 7
adj = np.array([
    [0, 1, 0, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 2, 0, 0, 1],
    [0, 0, 2, 0, 1, 0, 1],
    [1, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 1, 1, 0, 0, 0]
])
print("\nAdjacency Matrix:")
print(adj)
G = nx.MultiGraph()
for i in range(n):
    G.add_node(i)
edges = []
for i in range(n):
    for j in range(i + 1, n):
        for k in range(adj[i][j]):
            edge_name = f"e{len(edges)}"
            G.add_edge(i, j, key=edge_name)
            edges.append((edge_name, i, j))
print("\n" + "=" * 60)
print("MANUAL LINE GRAPH CONSTRUCTION")
print("=" * 60)
print("\nStep 1: Original edges")
for e in edges:
    print(f"{e[0]} : ({e[1]}, {e[2]})")
print("\nTotal edges:", len(edges))
L = nx.Graph()
print("\nStep 2: Each edge becomes a vertex in L(G)")
for e in edges:
    L.add_node(e[0])
print("Vertices in L(G):")
for e in edges:
    print(e[0], end=" ")
print()
print("\nStep 3: Check shared endpoints")
line_edges = []
for i in range(len(edges)):
    name1, u1, v1 = edges[i]
    for j in range(i + 1, len(edges)):
        name2, u2, v2 = edges[j]
        if (
            u1 == u2 or
            u1 == v2 or
            v1 == u2 or
            v1 == v2
        ):
            L.add_edge(name1, name2)
            line_edges.append((name1, name2))
            print(f"{name1} and {name2} share endpoint -> add edge")
print("\n" + "=" * 60)
print("RESULTING LINE GRAPH")
print("=" * 60)
print("\nVertices in L(G):")
print(list(L.nodes()))
print("\nEdges in L(G):")
print(list(L.edges()))
print("\nNumber of vertices in L(G):", L.number_of_nodes())
print("Number of edges in L(G):", L.number_of_edges())
plt.figure(figsize=(12, 5))
plt.subplot(121)
pos1 = nx.spring_layout(G)
nx.draw(G,pos1,with_labels=True,node_color="lightblue",node_size=800,font_size=10)
plt.title("Original Graph G")
plt.subplot(122)
pos2 = nx.spring_layout(L)
nx.draw(L,pos2,with_labels=True,node_color="lightgreen",node_size=800,font_size=10)
plt.title("Line Graph L(G)")
plt.tight_layout()
plt.show()