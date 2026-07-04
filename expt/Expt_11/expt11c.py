import networkx as nx
import matplotlib.pyplot as plt

sudoku = [
    [4, 0, 0, 0],
    [0, 0, 0, 4],
    [0, 4, 0, 0],
    [0, 0, 0, 0]
]

SIZE = 4
SUBGRID = 2

# MULTI GRAPH FOR MULTIPLE EDGES
G = nx.MultiDiGraph()

steps = []

def is_safe(board, row, col, num):
    for x in range(SIZE):
        if board[row][x] == num:
            return False
        if board[x][col] == num:
            return False

    start_row = (row // SUBGRID) * SUBGRID
    start_col = (col // SUBGRID) * SUBGRID

    for r in range(start_row, start_row + SUBGRID):
        for c in range(start_col, start_col + SUBGRID):
            if board[r][c] == num:
                return False

    return True

def solve(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:

                for num in range(1, SIZE + 1):

                    if is_safe(board, row, col, num):

                        steps.append(
                            f"Pick cell ({row+1},{col+1}) -> Assign {num}"
                        )

                        board[row][col] = num

                        if solve(board):
                            return True

                        board[row][col] = 0

                        steps.append(
                            f"Backtrack cell ({row+1},{col+1})"
                        )

                return False

    return True

print("\nInitial Sudoku:\n")

for row in sudoku:
    print(row)

solve(sudoku)

print("\nSteps:\n")

for step in steps:
    print(step)

print("\nSolved Sudoku:\n")

for row in sudoku:
    print(row)

# ADD NODES
for i in range(SIZE):
    for j in range(SIZE):
        node = i * SIZE + j
        G.add_node(node)

# MULTIPLE EDGES LOGIC
row_edges = []
col_edges = []
box_edges = []

for r1 in range(SIZE):
    for c1 in range(SIZE):

        node1 = r1 * SIZE + c1

        for r2 in range(SIZE):
            for c2 in range(SIZE):

                node2 = r2 * SIZE + c2

                if node1 < node2:

                    # SAME ROW
                    if r1 == r2:
                        G.add_edge(node1, node2, relation="row")
                        row_edges.append((node1, node2))

                    # SAME COLUMN
                    if c1 == c2:
                        G.add_edge(node1, node2, relation="column")
                        col_edges.append((node1, node2))

                    # SAME SUBGRID
                    if (
                        r1 // SUBGRID == r2 // SUBGRID
                        and
                        c1 // SUBGRID == c2 // SUBGRID
                    ):
                        G.add_edge(node1, node2, relation="box")
                        box_edges.append((node1, node2))

colors = ["red", "green", "skyblue", "yellow"]

node_colors = []
labels = {}
pos = {}

for i in range(SIZE):
    for j in range(SIZE):

        node = i * SIZE + j

        labels[node] = sudoku[i][j]

        node_colors.append(
            colors[sudoku[i][j] - 1]
        )

        pos[node] = (j, -i)

plt.figure(figsize=(8,8))

# DRAW NODES
nx.draw_networkx_nodes(
    G,
    pos,
    node_color=node_colors,
    node_size=2500,
    edgecolors='black',
    linewidths=2
)

# DRAW LABELS
nx.draw_networkx_labels(
    G,
    pos,
    labels=labels,
    font_size=16,
    font_weight='bold'
)

# ROW EDGES
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=row_edges,
    width=2,
    alpha=0.6,
    connectionstyle='arc3,rad=0.1'
)

# COLUMN EDGES
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=col_edges,
    width=2,
    alpha=0.6,
    connectionstyle='arc3,rad=-0.1'
)

# BOX EDGES
nx.draw_networkx_edges(
    G,
    pos,
    edgelist=box_edges,
    width=2,
    alpha=0.6,
    style='dashed',
    connectionstyle='arc3,rad=0.25'
)

plt.title(
    "Sudoku Solved using Multi Graph Coloring",
    fontsize=14
)

plt.axis('off')
plt.tight_layout()
plt.show()