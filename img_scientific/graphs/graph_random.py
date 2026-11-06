import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def all_pairs_undirected(nodes):
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i < j:
                yield u, v


def random_pairs_undirected(nodes, p, seed=42):
    rng = np.random.default_rng(seed)
    for edge in all_pairs_undirected(nodes):
        if rng.random() < p:
            yield edge


def make_random_graph(n, p, seed=42):
    _ = np.random.default_rng(seed)
    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(random_pairs_undirected(nodes, p))
    return G


random_graph = make_random_graph(10, 0.3)
len(random_graph.edges())  # 18

nx.draw_circular(random_graph, node_color="C3", node_size=1000, with_labels=True)
plt.show()
