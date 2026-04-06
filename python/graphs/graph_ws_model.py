import networkx as nx
import numpy as np
from networkx.algorithms.approximation import average_clustering


def sample_path_lengths(G, nodes=None, trials=1000):
    nodes = list(G) if nodes is None else list(nodes)
    rng = np.random.default_rng(42)
    pairs = rng.choice(nodes, (trials, 2))
    return [nx.shortest_path_length(G, *pair) for pair in pairs]


def estimate_path_length(G, nodes=None, trials=1000):
    return np.mean(sample_path_lengths(G, nodes, trials))


def read_graph(filename):
    G = nx.Graph()
    array = np.loadtxt(filename, dtype=int)
    G.add_edges_from(array)
    return G


# https://snap.stanford.edu/data/facebook_combined.txt.gz
fb = read_graph("../../data/facebook_combined.txtz")
n, m = len(fb), len(fb.edges())  # (4039, 88234)

C = average_clustering(fb)
L = estimate_path_length(fb)
k = round(2 * m / n)  # 44

lattice = nx.watts_strogatz_graph(n, k, p=0)
len(lattice), len(lattice.edges())
# (4039, 88858)

C, average_clustering(lattice)
# (0.615, 0.747)
L, estimate_path_length(lattice)
# (3.717, 47.088)
