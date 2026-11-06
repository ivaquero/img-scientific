"""Clustering-coefficient helper."""

from __future__ import annotations

import numpy as np
from scipy.special import comb

from .graph_random import all_pairs_undirected


def node_clustering(g, u):
    """Fraction of node ``u``'s neighbour pairs that are themselves connected."""
    neighbors = g[u]
    k = len(neighbors)
    if k < 2:
        return np.nan
    possible = comb(k, 2)
    exist = sum(bool(g.has_edge(v, w)) for v, w in all_pairs_undirected(neighbors))
    return exist / possible


def clustering_coefficient(g):
    """Average node clustering coefficient over the whole graph."""
    cu = [node_clustering(g, node) for node in g]
    return np.nanmean(cu)
