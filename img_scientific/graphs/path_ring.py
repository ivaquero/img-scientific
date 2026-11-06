"""Ring-lattice / Watts-Strogatz construction helpers (shared by WS, regular, Dijkstra charts)."""

from __future__ import annotations

import networkx as nx


def adjacent_edges(nodes, halfk):
    """Yield edges between each node and its ``halfk`` neighbours on a ring.

    ``halfk`` is the number of edges contributed from each node in one
    direction, so the ring-lattice degree is ``2 * halfk``.
    """
    n = len(nodes)
    for i, u in enumerate(nodes):
        for j in range(i + 1, i + halfk + 1):
            v = nodes[j % n]
            yield u, v


def make_ring_lattice(n, k):
    """Build a ring lattice with ``n`` nodes and degree ``k`` (``k`` even)."""
    g = nx.Graph()
    nodes = range(n)
    g.add_nodes_from(nodes)
    g.add_edges_from(adjacent_edges(nodes, k // 2))
    return g


def make_watts_strogatz(n, k, p, rng):
    """Watts-Strogatz small-world graph: ring lattice, then rewire each edge
    with probability ``p`` to a random non-neighbour (seeded via ``rng``)."""
    g = make_ring_lattice(n, k)
    for u, v in list(g.edges()):
        if rng.random() < p:
            candidates = [w for w in range(n) if w != u and not g.has_edge(u, w)]
            if candidates:
                w = candidates[rng.integers(len(candidates))]
                g.remove_edge(u, v)
                g.add_edge(u, w)
    return g
