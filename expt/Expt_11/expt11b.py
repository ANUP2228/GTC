import networkx as nx
import matplotlib.pyplot as plt
class Graph:
    def __init__(self, num_vertices):
        """
        Initialize a graph with given number of vertices
        
        Args:
            num_vertices: Number of vertices in the graph
        """
        self.num_vertices = num_vertices
        self.adjacency_list = [[] for _ in range(num_vertices)]
    
    def add_edge(self, u, v):
        """
        Add an undirected edge between vertices u and v
        
        Args:
            u: First vertex
            v: Second vertex
        """
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)
    
    def greedy_coloring(self):
        """
        Assign colors to vertices using greedy algorithm
        
        Returns:
            A list where result[i] is the color assigned to vertex i
        """
        result = [-1] * self.num_vertices
        
        result[0] = 0
        
        available = [False] * self.num_vertices
        
        for u in range(1, self.num_vertices):
            for i in self.adjacency_list[u]:
                if result[i] != -1:
                    available[result[i]] = True
            
            color = 0
            while available[color]:
                color += 1
            
            result[u] = color
            
            available = [False] * self.num_vertices
        
        return result
    
    def display_coloring(self, colors, start=0):
        """
        Display the vertex coloring result
        
        Args:
            colors: List of colors assigned to each vertex
            start: Starting vertex index to display
        """
        print("\nVertex Coloring Result:")
        print("-" * 40)
        for vertex in range(start, self.num_vertices):
            print(f"Vertex {vertex} --> Color {colors[vertex]}")
        
        num_colors = max(colors) + 1
        print("-" * 40)
        print(f"Total colors used: {num_colors}")
        
        print("\nColors assigned:")
        for color in range(num_colors):
            vertices_with_color = [v for v in range(start, self.num_vertices) if colors[v] == color]
            print(f"Color {color}: {vertices_with_color}")


def main():
    """Main function: Simple graph with 9 labeled vertices (1-9)"""
    print("\n" + "="*50)
    print("VERTEX COLORING - GREEDY ALGORITHM")
    print("="*50)

    edges = [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 6),
        (2, 3),
        (2, 5),
        (2, 6),
        (3, 4),
        (3, 5),
        (4, 7),
        (5, 8),
        (6, 9),
        (7, 8),
        (7, 9),
        (8, 9),
    ]

    num_vertices = max(max(edge) for edge in edges) + 1
    G = Graph(num_vertices)

    for u, v in edges:
        G.add_edge(u, v)

    print(" 0. RED ")
    print(" 1. BLUE ")
    print(" 2. GREEN ")
    print(" 3. YELLOW ")

    print("\nAdjacency List:")
    for v in range(1, G.num_vertices):
        print(f"Vertex {v}: {G.adjacency_list[v]}")

    colors = G.greedy_coloring()
    G.display_coloring(colors, start=1)

    is_valid = verify_coloring(G, colors, start=1)
    print(f"\nColoring is valid: {is_valid}")

    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(range(1, num_vertices))
    nx_graph.add_edges_from(edges)

    color_names = ["red", "blue", "green", "yellow", "orange", "purple", "cyan", "magenta"]
    color_map = [color_names[colors[v]] if colors[v] < len(color_names) else "gray" for v in range(1, num_vertices)]

    pos = {
        1: (-1, 2),
        2: (1, 2),
        3: (0, 1.5),
        4: (-1.6, 0.5),
        5: (1.6, 0.5),
        6: (0, 0),
        7: (-1, -2),
        8: (1, -2),
        9: (0, -3),
    }

    plt.figure(figsize=(8, 6))
    nx.draw(
        nx_graph,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=1200,
        font_size=12,
        edgecolors="black",
    )
    plt.title("Graph Coloring")
    plt.show()

def verify_coloring(G, colors, start=0):
    """
    Verify that the coloring is valid (no adjacent vertices have same color)
    
    Args:
        G: Graph object
        colors: List of colors assigned to vertices
        start: Starting vertex index to verify
    
    Returns:
        True if coloring is valid, False otherwise
    """
    for vertex in range(start, G.num_vertices):
        for neighbor in G.adjacency_list[vertex]:
            if colors[vertex] == colors[neighbor]:
                return False
    return True


if __name__ == "__main__":
    main()
