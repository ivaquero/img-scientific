import matplotlib.pyplot as plt
import networkx as nx
from .path_ring import adjacent_edges


def opposite_edges(nodes):
    n = len(nodes)
    for i, u in enumerate(nodes):
        j = i + n // 2
        v = nodes[j % n]
        yield u, v


def make_regular_graph(n, k):
    # a is the number of adjacent edges
    # b is the number of opposite edges (0 or 1)
    a, b = divmod(k, 2)

    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(adjacent_edges(nodes, a))
    # if k is odd, add opposite edges
    if b:
        if n % 2:
            msg = "Can not make a regular graph"
            raise ValueError(msg)
        G.add_edges_from(opposite_edges(nodes))
    return G


regular = make_regular_graph(10, 3)

nx.draw_circular(regular, node_color="C4", node_size=1000, with_labels=True)
plt.show()
