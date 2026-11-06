"""Breadth-first reachable-node set helper (complexity O(n + m))."""

from __future__ import annotations


def reachable_nodes_bfs(g, start):
    """Return every node reachable from ``start`` using a level-order BFS."""
    seen = set()
    nextlevel = {start}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in seen:
                seen.add(v)
                nextlevel.update(g[v])
    return seen
