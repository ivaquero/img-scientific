import networkx as nx
import numpy as np
from .path_ring import make_ring_lattice


def path_lengths(G):
    length_iter = nx.shortest_path_length(G)
    for _, dist_map in length_iter:
        yield from dist_map.values()


def characteristic_path_length(G):
    return np.mean(list(path_lengths(G)))


complete = nx.complete_graph(10)
characteristic_path_length(complete)  # 0.9
lattice = make_ring_lattice(1000, 10)
characteristic_path_length(lattice)  # 50.4
