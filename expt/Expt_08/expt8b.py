import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.graph = {}
        
    def add_edge(self, u, v):
        if u not in self.graph: self.graph[u] = []
        if v not in self.graph: self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    def get_edges(self):
        edges = []
        for u in self.graph:
            for v in self.graph[u]:
                if (v, u) not in edges:
                    edges.append((u, v))
        return edges

    def find_cycle(self):
        """Returns the first cycle found (Closed Path)."""
        visited = set()
        def dfs(node, parent, path):
            visited.add(node)
            path.append(node)
            for neighbor in self.graph[node]:
                if neighbor == parent: continue
                if neighbor in path:
                    idx = path.index(neighbor)
                    return path[idx:] + [neighbor]
                if neighbor not in visited:
                    result = dfs(neighbor, node, path.copy())
                    if result: return result
            return None

        for node in self.graph:
            if node not in visited:
                cycle = dfs(node, None, [])
                if cycle: return cycle
        return []

    def closed_trail(self):
        """Greedy approach to find a trail (no repeated edges)."""
        visited_edges = set()
        start = list(self.graph.keys())[0]
        trail, current = [start], start
        
        while True:
            found = False
            for neighbor in self.graph[current]:
                edge = tuple(sorted((current, neighbor)))
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    trail.append(neighbor)
                    current = neighbor
                    found = True
                    break
            if not found: break
        if trail[0] != trail[-1]: trail.append(trail[0])
        return trail

def draw_custom_graph(ax, graph, pos, title):
    for u, v in graph.get_edges():
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color="black", lw=2, zorder=1)
    for node, coords in pos.items():
        ax.add_patch(plt.Circle(coords, 0.15, color="white", ec="black", lw=2, zorder=2))
        ax.text(coords[0], coords[1], node, ha='center', va='center', fontweight='bold', zorder=3)
    ax.set_title(title, fontsize=14)
    ax.set_aspect('equal')
    ax.axis('off')


G1 = Graph()
for u, v in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]:
    G1.add_edge(u, v)
pos1 = {"A": (-1, 1), "B": (1, 1), "C": (1, -1), "D": (-1, -1)}

G2 = Graph()
for u, v in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "A")]:
    G2.add_edge(u, v)
for u, v in [("B", "D"), ("D", "F"), ("F", "H"), ("H", "B")]:
    G2.add_edge(u, v)

pos2 = {
    "A": (-1, 1),   "C": (1, 1),  "E": (1, -1), "G": (-1, -1),  
    "B": (0, 1),   "D": (1, 0),  "F": (0, -1),  "H": (-1, 0)    
}

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
draw_custom_graph(ax[0], G1, pos1, "GRAPH (a): Square")
draw_custom_graph(ax[1], G2, pos2, "GRAPH (b): Inscribed Diamond")
plt.tight_layout()
plt.show()

print("--- Analysis Results ---")
for name, g in [("Graph (a)", G1), ("Graph (b)", G2)]:
    print(f"\n{name}:")
    print(f"Closed Path (Cycle):  {' -> '.join(g.find_cycle())}")
    print(f"Closed Trail:         {' -> '.join(g.closed_trail())}")