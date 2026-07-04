import networkx as nx
import matplotlib.pyplot as plt

steps1 = []
steps2 = []

def hamiltonian_circuit(G, steps):
    n = len(G.nodes())
    def solve(path):
        if len(path) == n:
            if G.has_edge(path[-1], path[0]):
                return path + [path[0]]
            return None
        for neighbor in sorted(list(G.neighbors(path[-1]))):
            if neighbor not in path:
                new_path = path + [neighbor]
                if new_path not in steps:
                    steps.append(new_path)
                result = solve(new_path)
                if result:
                    return result
        return None

    nodes = sorted(list(G.nodes()))
    for start in nodes:
        steps.append([start])
        result = solve([start])
        if result:
            if result not in steps:
                steps.append(result)
            return result
    return None

G1 = nx.Graph()
edges1 = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')]
G1.add_edges_from(edges1)

pos1 = {
    'A': (0, 1),
    'B': (1, 1),
    'C': (1, 0),
    'D': (0, 0)
}

cycle1 = hamiltonian_circuit(G1, steps1)
print("Graph (a) Hamiltonian Circuit:")
print(" -> ".join(map(str, cycle1)) if cycle1 else "No circuit found")

cols = 3
rows = (len(steps1) + cols - 1) // cols
fig1, axes1 = plt.subplots(rows, cols, figsize=(15, rows * 4))
axes1 = axes1.flatten()

for i in range(len(axes1)):
    ax = axes1[i]
    if i < len(steps1):
        step = steps1[i]
        nx.draw_networkx(G1, pos1, node_color='white', edgecolors='black', node_size=800, ax=ax)
        step_edges = list(zip(step, step[1:]))
        nx.draw_networkx_edges(G1, pos1, edgelist=step_edges, edge_color='red', width=3, ax=ax)
        ax.set_title(f"Step {i+1}: {'-'.join(step)}")
    ax.axis('off')
plt.tight_layout()

G2 = nx.Graph()
edges2 = [
    ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), 
    ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'A'),
    ('B', 'D'), ('D', 'F'), ('F', 'H'), ('H', 'B') 
]
G2.add_edges_from(edges2)

pos2 = {
    'A': (-1, 1), 'C': (1, 1), 'E': (1, -1), 'G': (-1, -1), 
    'H': (-1, 0), 'B': (0, 1), 'D': (1, 0), 'F': (0, -1)    
}

cycle2 = hamiltonian_circuit(G2, steps2)
print("\nGraph (b) Hamiltonian Circuit:")
print(" -> ".join(map(str, cycle2)) if cycle2 else "No circuit found")

cols = 4
rows = (len(steps2) + cols - 1) // cols
fig2, axes2 = plt.subplots(rows, cols, figsize=(20, rows * 4))
axes2 = axes2.flatten()

for i in range(len(axes2)):
    ax = axes2[i]
    if i < len(steps2):
        step = steps2[i]
        nx.draw_networkx(G2, pos2, node_color='white', edgecolors='black', node_size=600, ax=ax, font_size=10)
        step_edges = list(zip(step, step[1:]))
        nx.draw_networkx_edges(G2, pos2, edgelist=step_edges, edge_color='red', width=3, ax=ax)
        ax.set_title(f"Step {i+1}", fontsize=10)
    ax.axis('off')
plt.tight_layout()

plt.show()