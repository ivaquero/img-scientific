import random

import networkx as nx
from .graph_random import all_pairs_undirected


def m_pairs(nodes, m):
    pairs = list(all_pairs_undirected(nodes))
    return random.sample(pairs, m)


def make_m_graph(n, m):
    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(m_pairs(nodes, m))
    return G


m_graph = make_m_graph(10, 15)

nx.draw_circular(m_graph, node_color="C4", node_size=1000, with_labels=True)
