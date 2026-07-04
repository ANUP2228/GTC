import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def kruskal_manual(edges):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    pos = {'A': (0, 2), 'B': (1, 2), 'C': (2, 2), 'D': (3, 2),
           'E': (0, 1), 'F': (1, 1), 'G': (2, 1), 'H': (3, 1),
           'I': (0, 0), 'J': (1, 0), 'K': (2, 0), 'L': (3, 0)}

    sorted_edges = sorted(edges, key=lambda x: x[2])
    mst_edges = []
    step_images = []

    print("\nKRUSKAL ALGORITHM STEP BY STEP\n")

    step = 1

    for u, v, w in sorted_edges:
        temp = nx.Graph()
        temp.add_edges_from(mst_edges)
        cycle = False

        if u in temp.nodes() and v in temp.nodes() and nx.has_path(temp, u, v):
            cycle = True

        print(f"STEP {step}")
        print(f"Checking Edge ({u},{v}) = {w}")

        fig, ax = plt.subplots(figsize=(4, 3))

        nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=2500, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=11, ax=ax)

        if not cycle:
            mst_edges.append((u, v))
            print("Edge Accepted\n")
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='red', width=3, ax=ax)
            edge_labels = {edge: G[edge[0]][edge[1]]['weight'] for edge in mst_edges}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)
            title = f"STEP {step}: Accepted ({u},{v})"
        else:
            print("Edge Rejected (Cycle Formed)\n")
            nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='red', width=3, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='gray', style='dashed', width=2, ax=ax)
            edge_labels = {edge: G[edge[0]][edge[1]]['weight'] for edge in mst_edges}
            edge_labels[(u, v)] = w
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, ax=ax)
            title = f"STEP {step}: Rejected ({u},{v})"

        fig.tight_layout()
        ax.set_title(title, fontsize=9)
        ax.axis('off')
        fig.canvas.draw()

        buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        image = buf.reshape(fig.canvas.get_width_height()[::-1] + (4,))
        step_images.append((image, title))
        plt.close(fig)

        step += 1

        if len(mst_edges) == len(G.nodes()) - 1:
            break

    print("\nFINAL MST\n")
    total = 0
    for u, v in mst_edges:
        weight = G[u][v]['weight']
        total += weight
        print(f"{u} -- {v} = {weight}")
    print(f"\nTotal Weight = {total}")

    cols = 4
    rows = (len(step_images) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3 * rows))
    axes = axes.flatten() if rows > 1 or cols > 1 else [axes]

    for ax, (image, title) in zip(axes, step_images):
        ax.imshow(image)
        ax.set_title(title, fontsize=8)
        ax.axis('off')

    for ax in axes[len(step_images):]:
        ax.axis('off')

    fig.suptitle('Kruskal Algorithm: All Steps in One Image', fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()


edges = [
    ('A', 'B', 2), ('B', 'C', 3), ('C', 'D', 1),
    ('A', 'E', 3), ('B', 'F', 1), ('C', 'G', 2), ('D', 'H', 5),
    ('E', 'F', 4), ('F', 'G', 3), ('G', 'H', 4),
    ('E', 'I', 4), ('F', 'J', 2), ('G', 'K', 4), ('H', 'L', 3),
    ('I', 'J', 3), ('J', 'K', 3), ('K', 'L', 1)
]

kruskal_manual(edges)