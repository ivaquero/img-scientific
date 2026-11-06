import numpy as np
from .graph_random import all_pairs_undirected
from .path_ring import make_ring_lattice
from scipy.special import comb


def node_clustering(G, u):
    neighbors = G[u]
    k = len(neighbors)
    if k < 2:
        return np.nan
    possible = comb(k, 2)
    exist = sum(bool(G.has_edge(v, w)) for v, w in all_pairs_undirected(neighbors))
    return exist / possible


lattice = make_ring_lattice(10, 4)
node_clustering(lattice, 1)  # 0.5


def clustering_coefficient(G):
    cu = [node_clustering(G, node) for node in G]
    return np.nanmean(cu)


clustering_coefficient(lattice)  # 0.5
