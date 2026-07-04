import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def get_adjacency_matrix():
    """Hardcoded adjacency matrix (7x7)"""
    matrix = [
        [0, 1, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 2, 0, 0, 1],
        [0, 0, 2, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 0, 0]
    ]
    return np.array(matrix)

def construct_line_graph_with_networkx(adj_matrix):
    """Method 1: Construct line graph using NetworkX built-in function"""
    
    print("\n" + "="*60)
    print("METHOD 1: Using NetworkX built-in function")
    print("="*60)

    G = nx.from_numpy_array(adj_matrix)

    print(f"\nOriginal Graph G:")
    print(f" Vertices: {G.number_of_nodes()}")
    print(f" Edges: {list(G.edges())}")
    print(f" Number of edges: {G.number_of_edges()}")

    L_G = nx.line_graph(G)

    print(f"\nLine Graph L(G):")
    print(f" Vertices (each represents an edge from G): {L_G.number_of_nodes()}")
    print(f" Vertex labels: {list(L_G.nodes())}")
    print(f" Edges in L(G): {list(L_G.edges())}")
    print(f" Number of edges in L(G): {L_G.number_of_edges()}")

    return G, L_G

def visualize_graphs(G, L_G, method_name):
    """Visualize original graph and its line graph"""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    pos_g = nx.spring_layout(G, seed=42)

    ax1.set_title(f'Original Graph G\n({method_name})', fontsize=14, fontweight='bold')

    nx.draw(
        G,
        pos_g,
        ax=ax1,
        with_labels=True,
        node_color='lightblue',
        node_size=800,
        font_size=12,
        font_weight='bold',
        edge_color='gray',
        width=2
    )

    pos_lg = nx.spring_layout(L_G, seed=42)

    ax2.set_title(f'Line Graph L(G)\n({method_name})', fontsize=14, fontweight='bold')

    nx.draw(
        L_G,
        pos_lg,
        ax=ax2,
        with_labels=True,
        node_color='lightcoral',
        node_size=1200,
        font_size=9,
        font_weight='bold',
        edge_color='gray',
        width=2
    )

    plt.tight_layout()

def main():

    print("="*60)
    print("LINE GRAPH CONSTRUCTION")
    print("="*60)

    print("\nA line graph L(G) of a graph G:")
    print(" - Each edge in G becomes a vertex in L(G)")
    print(" - Two vertices in L(G) are adjacent if their corresponding")
    print("   edges in G share a common endpoint")

    print("="*60)

    try:

        adj_matrix = get_adjacency_matrix()

        print("\nAdjacency Matrix:")
        print(adj_matrix)

        G1, L_G1 = construct_line_graph_with_networkx(adj_matrix)

        visualize_graphs(G1, L_G1, "NetworkX Method")

        plt.show()

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()