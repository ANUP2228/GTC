import matplotlib.pyplot as plt
import networkx as nx

def visualize_mst_builtin(edges_data):
    G = nx.Graph()
    G.add_weighted_edges_from(edges_data)
    
    pos = {'A':(0,2), 'B':(1,2), 'C':(2,2), 'D':(3,2),
           'E':(0,1), 'F':(1,1), 'G':(2,1), 'H':(3,1),
           'I':(0,0), 'J':(1,0), 'K':(2,0), 'L':(3,0)}

    mst = nx.minimum_spanning_tree(G, weight='weight')
    mst_edges = list(mst.edges())
    mst_cost = mst.size(weight='weight')
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), constrained_layout=True)
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', edgecolors='black', node_size=250, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=list(G.edges()), edge_color='lightgray', width=0.5, style='dashed', ax=ax)
    
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='green', width=2, ax=ax)
    
    ax.set_title(f"Minimum Spanning Tree\nTotal Cost: {mst_cost}", fontsize=12)
    ax.axis('off')
    
    print(f"MST Total Cost: {mst_cost}")
    print(f"MST Edges: {mst_edges}")
    plt.show()

G = nx.Graph()
G.add_nodes_from(['A','B','C','D','E','F','G','H','I','J','K','L'])

edges_data = [
    ('A','B',2), ('B','C',3), ('C','D',1),
    ('A','E',3), ('B','F',1), ('C','G',2), ('D','H',5),
    ('E','F',4), ('F','G',3), ('G','H',4),
    ('E','I',4), ('F','J',2), ('G','K',4), ('H','L',3),
    ('I','J',3), ('J','K',3), ('K','L',1)
]

visualize_mst_builtin(edges_data)
