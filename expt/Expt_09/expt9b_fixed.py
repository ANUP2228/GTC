import matplotlib.pyplot as plt
import math

def draw_edge(ax, p1, p2, radius=0.18, color='black', linewidth=2, alpha=1.0):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    dist = math.sqrt(dx**2 + dy**2)
    ux, uy = dx / dist, dy / dist
    ax.plot([x1 + ux * radius, x2 - ux * radius], 
            [y1 + uy * radius, y2 - uy * radius], color=color, linewidth=linewidth, alpha=alpha, zorder=2)

class Graph:
    def __init__(self, vertices, labels):
        self.V = vertices
        self.labels = labels
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]
        self.original_graph = None

    def add_edge(self, u, v, count=1):
        self.graph[u][v] += count
        self.graph[v][u] += count

    def has_euler_circuit(self):
        visited = [False] * self.V
        start = 0
        stack = [start]
        visited[start] = True
        while stack:
            u = stack.pop()
            for v in range(self.V):
                if self.graph[u][v] > 0 and not visited[v]:
                    visited[v] = True
                    stack.append(v)
        if not all(visited): return False
        return all(sum(row) % 2 == 0 for row in self.graph)

    def find_euler_circuit_steps(self):
        """Find Euler circuit and return steps for visualization"""
        if not self.has_euler_circuit(): return None, []
        
        g = [row[:] for row in self.graph]
        path, circuit = [0], []
        steps = []  # Store (current_path, circuit_so_far)
        steps.append((list(path), list(circuit)))
        
        while path:
            u = path[-1]
            found = False
            for v in range(self.V):
                if g[u][v] > 0:
                    g[u][v] -= 1
                    g[v][u] -= 1
                    path.append(v)
                    found = True
                    steps.append((list(path), list(circuit)))
                    break
            if not found: 
                circuit.append(path.pop())
                steps.append((list(path), list(circuit)))
        
        result = [self.labels[i] for i in circuit[::-1]]
        return result, steps

    def find_euler_circuit(self):
        circuit, _ = self.find_euler_circuit_steps()
        return circuit

    def draw(self, ax, pos, title):
        for i in range(self.V):
            for j in range(i + 1, self.V):
                if self.graph[i][j] > 0:
                    draw_edge(ax, pos[i], pos[j])
        for i, node_pos in pos.items():
            ax.add_patch(plt.Circle(node_pos, 0.18, color='white', ec='black', lw=2, zorder=5))
            ax.text(node_pos[0], node_pos[1], self.labels[i], ha='center', va='center', zorder=6)
        ax.set_title(title)
        ax.set_aspect('equal')
        ax.axis('off')

    def draw_step(self, ax, pos, title, path, circuit, all_edges):
        """Draw graph with current path and circuit highlighted"""
        # Draw all edges in light gray
        for i in range(self.V):
            for j in range(i + 1, self.V):
                if self.graph[i][j] > 0:
                    draw_edge(ax, pos[i], pos[j], color='lightgray', linewidth=1, alpha=0.3)
        
        # Draw edges in circuit (completed) in green
        for i in range(len(circuit) - 1):
            u, v = circuit[i], circuit[i+1]
            draw_edge(ax, pos[u], pos[v], color='green', linewidth=3, alpha=0.8)
        
        # Draw current path in red
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            draw_edge(ax, pos[u], pos[v], color='red', linewidth=2.5, alpha=1.0)
        
        # Draw nodes
        current_node = path[-1] if path else None  # Fix: check if path is not empty
        for i, node_pos in pos.items():
            color = 'yellow' if current_node is not None and i == current_node else 'white'
            ax.add_patch(plt.Circle(node_pos, 0.18, color=color, ec='black', lw=2, zorder=5))
            ax.text(node_pos[0], node_pos[1], self.labels[i], ha='center', va='center', fontweight='bold', zorder=6)
        
        ax.set_title(title, fontsize=10)
        ax.set_aspect('equal')
        ax.axis('off')


G1 = Graph(4, ["A", "B", "C", "D"])
for u, v in [(0,1), (1,2), (2,3), (3,0)]: G1.add_edge(u, v)
pos1 = {0: (-1, 1), 1: (1, 1), 2: (1, -1), 3: (-1, -1)}

G2 = Graph(8, ["A", "B", "C", "D", "E", "F", "G", "H"])
for u, v in [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,0)]: G2.add_edge(u, v)
for u, v in [(1,3), (3,5), (5,7), (7,1)]: G2.add_edge(u, v)
pos2 = {
    0: (-1, 1), 2: (1, 1), 4: (1, -1), 6: (-1, -1), 
    7: (-1, 0), 1: (0, 1), 3: (1, 0), 5: (0, -1)    
}

# Original combined view
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
G1.draw(axes[0], pos1, "GRAPH (a)")
G2.draw(axes[1], pos2, "GRAPH (b)")

for name, g in [("Graph A", G1), ("Graph B", G2)]:
    circuit = g.find_euler_circuit()
    print(f"{name} Euler Circuit: {circuit if circuit else 'None'}")

plt.tight_layout()
plt.show()

# STEPWISE VISUALIZATION FOR GRAPH A
print("\n" + "="*50)
print("STEPWISE VISUALIZATION: GRAPH A")
print("="*50)

circuit_a, steps_a = G1.find_euler_circuit_steps()
print(f"Final Euler Circuit: {circuit_a}\n")

# Show every few steps
step_indices = list(range(0, len(steps_a), max(1, len(steps_a)//8))) + [len(steps_a)-1]
step_indices = sorted(set(step_indices))

cols = 4
rows = (len(step_indices) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(16, 3*rows))
axes = axes.flatten()

for idx, step_num in enumerate(step_indices):
    path, circuit = steps_a[step_num]
    path_labels = [G1.labels[i] for i in path]
    circuit_labels = [G1.labels[i] for i in circuit]
    
    G1.draw_step(axes[idx], pos1, 
                 f"Step {step_num}\nPath: {path_labels}\nCircuit: {circuit_labels}",
                 path, circuit, G1.graph)

for idx in range(len(step_indices), len(axes)):
    axes[idx].axis('off')

plt.tight_layout()
plt.show()

# STEPWISE VISUALIZATION FOR GRAPH B
print("\n" + "="*50)
print("STEPWISE VISUALIZATION: GRAPH B")
print("="*50)

circuit_b, steps_b = G2.find_euler_circuit_steps()
print(f"Final Euler Circuit: {circuit_b}\n")

# Show every few steps
step_indices_b = list(range(0, len(steps_b), max(1, len(steps_b)//12))) + [len(steps_b)-1]
step_indices_b = sorted(set(step_indices_b))

cols = 4
rows = (len(step_indices_b) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(16, 3*rows))
axes = axes.flatten()

for idx, step_num in enumerate(step_indices_b):
    path, circuit = steps_b[step_num]
    path_labels = [G2.labels[i] for i in path]
    circuit_labels = [G2.labels[i] for i in circuit]
    
    G2.draw_step(axes[idx], pos2, 
                 f"Step {step_num}\nPath: {path_labels[:3]}...\nCircuit: {circuit_labels[:3]}...",
                 path, circuit, G2.graph)

for idx in range(len(step_indices_b), len(axes)):
    axes[idx].axis('off')

plt.tight_layout()
plt.show()
