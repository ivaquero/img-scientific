"""Connectivity helpers (undirected + strongly-connected directed)."""

from __future__ import annotations

import numpy as np


def reachable_nodes(g, start, directed=False):
    """Depth-first set of nodes reachable from ``start`` (optionally directed)."""
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            if directed:
                stack.extend(g.successors(node))
            else:
                stack.extend(g.neighbors(node))
    return seen


def is_connected(g):
    """True when every node is reachable from the first node (undirected)."""
    start = next(iter(g))
    return len(reachable_nodes(g, start)) == len(g)


def is_connected_digraph(g):
    """True when the digraph is strongly connected (every start reaches all)."""
    return all(len(reachable_nodes(g, start, directed=True)) >= len(g) for start in g)


def prob_connected(g, iters=100):
    """Fraction of ``iters`` connectivity checks that succeeded."""
    tf = [is_connected(g) for _ in range(iters)]
    return np.mean(tf)
