import networkx as nx

def analyze_graph(name, G, start_node):
   
    nodes = list(G.nodes())
    
    
    cycle = nx.find_cycle(G, source=start_node)
    path_nodes = [u for u, v in cycle] + [start_node]
    
    print(f"\n--- {name} ---")
    print("Closed Walk :", " -> ".join(path_nodes))
    print("Closed Path :", " -> ".join(path_nodes)) 
    print("Closed Trail:", " -> ".join(path_nodes)) 

ga = nx.Graph()
ga.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])

gb = nx.Graph()
gb.add_edges_from([("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), 
                   ("E", "F"), ("F", "G"), ("G", "H"), ("H", "A")])
gb.add_edges_from([("B", "D"), ("D", "F"), ("F", "H"), ("H", "B")])

analyze_graph("GRAPH A (Square)", ga, "A")
analyze_graph("GRAPH B (Square + Diamond)", gb, "A")