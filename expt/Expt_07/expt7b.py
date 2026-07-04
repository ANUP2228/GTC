import matplotlib.pyplot as plt
import heapq
import networkx as nx

graph = {
    'A': {'B': 4, 'C': 6, 'D': 5},
    'B': {'A': 4, 'C': 1, 'E': 7},
    'C': {'A': 6, 'B': 1, 'D': 2, 'F': 4, 'E': 5},
    'D': {'A': 5, 'C': 2, 'F': 5},
    'E': {'B': 7, 'C': 5, 'F': 1, 'G': 6},
    'F': {'C': 4, 'D': 5, 'E': 1, 'G': 8},
    'G': {'E': 6, 'F': 8}
}

edges = []
seen = set()
for u, neighbors in graph.items():
    for v, w in neighbors.items():
        if (v, u) not in seen:
            edges.append((u, v, w))
            seen.add((u, v))
            seen.add((v, u))

def dijkstra_table(graph, source):
    pq = [(0, source)]
    dist = {node: float('inf') for node in graph}
    parent = {node: None for node in graph}
    visited = set()
    dist[source] = 0
    step = 0
    nodes = sorted(graph.keys())

    print("\nDijkstra Table:\n")
    print("Step | Uᵢ            | " + " | ".join(str(n) for n in nodes))
    print("-" * 90)

    while pq:
        current_dist, u = heapq.heappop(pq)
        if u in visited:
            continue

        visited.add(u)

        row = []
        for n in nodes:
            if dist[n] == float('inf'):
                row.append("∞")
            elif parent[n] is None:
                row.append(f"{dist[n]}")
            else:
                row.append(f"{dist[n]}({parent[n]})")

        print(f"{step:<4} | {str(sorted(visited)):<15} | " + " | ".join(row))

        for v, weight in graph[u].items():
            if v not in visited and dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

        step += 1


def dijkstra(graph, source, target):
    pq = [(0, source)]
    dist = {node: float('inf') for node in graph}
    parent = {node: None for node in graph}
    dist[source] = 0

    while pq:
        current_dist, u = heapq.heappop(pq)
        if u == target:
            break

        if current_dist > dist[u]:
            continue

        for v, weight in graph[u].items():
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, dist[target]

source = 'A'
target = 'G'

dijkstra_table(graph, source)
path, distance = dijkstra(graph, source, target)

print("\nShortest Path:", path)
print("Total Cost:", distance)

G = nx.Graph()
G.add_weighted_edges_from(edges)

pos = {
    'A': (-1, 1),
    'B': (0, 2),
    'C': (0, 1),
    'D': (0, 0),
    'E': (1, 1.5),
    'F': (1, 0.5),
    'G': (2, 1)
}

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
nx.draw(G, pos, with_labels=True, node_size=800)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Original Graph")

plt.subplot(1, 2, 2)
nx.draw(G, pos, with_labels=True, node_size=800, alpha=0.3)
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title(f"Shortest Path\n{path} | Cost = {distance}")
plt.tight_layout()
plt.show()
