"""Reachability with neighbour pre-check (constant-factor speedup helper)."""

from __future__ import annotations


def reachable_nodes_precheck(g, start):
    """DFS reachable set that filters already-seen nodes before extending."""
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            neighbors = set(g[node]) - seen
            stack.extend(neighbors)
    return seen
