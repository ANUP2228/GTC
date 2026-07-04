import networkx as nx
import matplotlib.pyplot as plt

def get_spanning_subgraph(G, edges_to_keep):
    S = nx.Graph()
    S.add_nodes_from(G.nodes())
    for u, v in G.edges():
        if (u, v) in edges_to_keep or (v, u) in edges_to_keep:
            S.add_edge(u, v)
    return S

def get_induced_subgraph(G, nodes_to_keep):
    I = nx.Graph()
    I.add_nodes_from(nodes_to_keep)
    for u, v in G.edges():
        if u in nodes_to_keep and v in nodes_to_keep:
            I.add_edge(u, v)
    return I

def get_edge_subgraph(G, edges_to_keep):
    E_sub = nx.Graph()
    for u, v in edges_to_keep:
        if G.has_edge(u, v):
            E_sub.add_edge(u, v)
    return E_sub

G = nx.Graph()
edges = [(1,2), (1,3), (2,3), (1,4), (2,5), (3,4), (3,5), (1,6), (2,6), (4,7), (5,8), (7,8), (7,9), (8,9), (6,9)]
G.add_edges_from(edges)

pos = {
    1: (-1, 2), 2: (1, 2), 3: (0, 1.5),
    4: (-1.6, 0.5), 5: (1.6, 0.5), 6: (0, 0),
    7: (-1, -2), 8: (1, -2), 9: (0, -3)
}

removed = {(1, 3), (2, 3), (7, 8), (6, 9)}
keep_span = [e for e in edges if e not in removed and e[::-1] not in removed]
S = get_spanning_subgraph(G, keep_span)

I = get_induced_subgraph(G, {1, 2, 3, 4, 5})

E = get_edge_subgraph(G, [(1,2), (2,5), (5,8), (8,9)])

plt.figure(figsize=(12, 10))

plt.subplot(2, 2, 1)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=600)
plt.title("Original Graph (G)")

plt.subplot(2, 2, 2)
nx.draw(S, pos, with_labels=True, node_color='lightgreen', node_size=600)
plt.title("Manual Spanning Subgraph\n(All nodes, subset of edges)")

plt.subplot(2, 2, 3)
nx.draw(I, pos, with_labels=True, node_color='salmon', node_size=600)
plt.title("Manual Induced Subgraph\n(Nodes 1-5 + all internal edges)")

plt.subplot(2, 2, 4)
nx.draw(E, pos, with_labels=True, node_color='khaki', node_size=600)
plt.title("Manual Edge Subgraph\n(Edges (1,2), (2,5), (5,8), (8,9))")

plt.tight_layout()
plt.show()