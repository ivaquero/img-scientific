"""Level-sweeping shortest-path (Dijkstra for unit-weight edges) helper."""

from __future__ import annotations


def shortest_path_dijkstra(g, source):
    """BFS-by-level shortest distances from ``source`` for equal-weight edges.

    A fast alternative to ``nx.shortest_path_length`` on unweighted graphs.
    """
    new_dist = 0
    dist = {}
    nextlevel = {source}
    while nextlevel:
        thislevel = nextlevel
        nextlevel = set()
        for v in thislevel:
            if v not in dist:
                dist[v] = new_dist
                nextlevel.update(g[v])
        new_dist += 1
    return dist
