"""Sampled path-length estimation + edge-list graph loader (helpers)."""

from __future__ import annotations

import networkx as nx
import numpy as np


def sample_path_lengths(g, rng, nodes=None, trials=1000):
    """Shortest-path lengths for ``trials`` random node pairs (seeded ``rng``)."""
    nodes = list(g) if nodes is None else list(nodes)
    pairs = rng.choice(nodes, (trials, 2))
    return [nx.shortest_path_length(g, *pair) for pair in pairs]


def estimate_path_length(g, rng, nodes=None, trials=1000):
    """Mean of ``sample_path_lengths`` -- a cheap characteristic path length."""
    return np.mean(sample_path_lengths(g, rng, nodes, trials))


def read_graph(filename):
    """Build an undirected graph from an edge-list file (two ints per line)."""
    g = nx.Graph()
    array = np.loadtxt(filename, dtype=int)
    g.add_edges_from(array)
    return g
