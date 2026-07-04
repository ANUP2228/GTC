import networkx as nx
import matplotlib.pyplot as plt

G1= nx.Graph()
G1.add_nodes_from([1,2,3,4,5])
G1.add_edges_from([(1,2),(1,3),(1,4),(2,3),(1,5),(2,4),(2,5),(3,4),(3,5),(4,5)])

G2= nx.Graph()
G2.add_nodes_from([1,2,3,4,5])
G2.add_edges_from([(1,2),(2,3),(3,4),(4,5),(5,1)])


G3= nx.Graph()
G3.add_nodes_from([1,2])
G3.add_nodes_from([3,4,5])
G3.add_edges_from([(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)])


G4= nx.Graph()
G4.add_nodes_from([1,2,3,4,5])
G4.add_edges_from([(1,2),(2,3),(3,4),(4,5)])


plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
nx.draw(G1, with_labels=True,node_color='green')
plt.title("K5 (Complete Graph)")

plt.subplot(2, 2, 2)
nx.draw(G2, with_labels=True,node_color='red')
plt.title("C5 (Cycle Graph)")

plt.subplot(2, 2, 4)
pos={}
pos[1]=(0,1)
pos[2]=(1,1)
pos[3]=(0,0)
pos[4]=(1,0)
pos[5]=(2,0)
nx.draw(G3 ,pos, with_labels=True,node_color='yellow')
plt.title("K2,3 (Complete Bipartite Graph)")

plt.subplot(2, 2, 3)
nx.draw(G4, with_labels=True,node_color='purple')
plt.title("P5 (Path Graph)")

plt.tight_layout()
plt.show()
