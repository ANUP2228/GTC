import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, step, degrees):
    plt.figure(figsize=(8,6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=400,
            font_weight='bold',
            edge_color='black')
    plt.title(f"Step {step}  | Remaining degrees: {degrees}")
    plt.show()


def havel_hakimi_steps(degree_sequence):

    if sum(degree_sequence) % 2 != 0:
        print(f"Sequence {degree_sequence} is NOT graphical (Odd Sum)")
    
    nodes = [[deg, i] for i, deg in enumerate(degree_sequence)]
    G = nx.Graph()
    G.add_nodes_from(range(len(degree_sequence)))

    step = 1

    while True:
        nodes.sort(key=lambda x: x[0], reverse=True)

        if nodes[0][0] == 0:
            print("Graph realized successfully")
            break

        d, u = nodes.pop(0)

        if d > len(nodes):
            print(f"FAILED at step {step} → Not graphical")
            draw_graph(G, step, [n[0] for n in nodes])
            return

        for i in range(d):
            nodes[i][0] -= 1
            v = nodes[i][1]
            G.add_edge(u, v)

            if nodes[i][0] < 0:
                print(f"Negative degree at step {step} → Not graphical")
                draw_graph(G, step, [n[0] for n in nodes])
                return

        draw_graph(G, step, [n[0] for n in nodes])
        step += 1

seq = [5,4,4,2,2,1,1]
havel_hakimi_steps(seq)