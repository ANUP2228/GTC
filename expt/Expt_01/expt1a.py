import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.complete_graph(5)

G2 = nx.cycle_graph(5)

G3 = nx.complete_bipartite_graph(2, 3)

G4 = nx.path_graph(5)

plt.figure(figsize=(10, 8))
plt.subplot(2, 2, 1)
nx.draw(G1, with_labels=True, node_color='green')
plt.title("K5 (Complete Graph)")

plt.subplot(2, 2, 2)
nx.draw(G2, with_labels=True, node_color='red')
plt.title("C5 (Cycle Graph)")

plt.subplot(2, 2, 4)
pos={}
pos[0]=(0,1)
pos[1]=(1,1)
pos[2]=(0,0)
pos[3]=(1,0)
pos[4]=(2,0)
nx.draw(G3, pos, with_labels=True, node_color='yellow')
plt.title("K2,3 (Complete Bipartite Graph)")

plt.subplot(2, 2, 3)
nx.draw(G4, with_labels=True, node_color='purple')
plt.title("P5 (Path Graph)")

plt.tight_layout()
plt.show()
