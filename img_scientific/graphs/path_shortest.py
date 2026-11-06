"""Characteristic (mean) path length helper."""

from __future__ import annotations

import networkx as nx
import numpy as np


def path_lengths(g):
    """Yield the length of every shortest path in the graph (all source/target)."""
    length_iter = nx.shortest_path_length(g)
    for _, dist_map in length_iter:
        yield from dist_map.values()


def characteristic_path_length(g):
    """Mean shortest-path length over all reachable node pairs."""
    return np.mean(list(path_lengths(g)))
