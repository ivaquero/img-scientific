"""Shared graph-theory primitives for the ``graphs/`` topic.

Mirrors ``julia/graphs/_helpers.jl``: the reusable ring-lattice / Watts-Strogatz
builders and the clustering / characteristic-path metrics live here (underscore
prefixed, so the spec-driven loader never treats them as charts), while each
chart file keeps only its single ``@chart`` entry point and any one-off shims it
is the sole consumer of.
"""

from __future__ import annotations

import networkx as nx
import numpy as np
from scipy.special import comb

# --- edge / pair enumeration -------------------------------------------------


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


def all_pairs_undirected(nodes):
    """Yield each unordered pair ``(u, v)`` exactly once (``i < j``)."""
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i < j:
                yield u, v


# --- graph builders ----------------------------------------------------------


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


# --- path metrics ------------------------------------------------------------


def path_lengths(g):
    """Yield the length of every shortest path in the graph (all source/target)."""
    length_iter = nx.shortest_path_length(g)
    for _, dist_map in length_iter:
        yield from dist_map.values()


def characteristic_path_length(g):
    """Mean shortest-path length over all reachable node pairs."""
    return np.mean(list(path_lengths(g)))


# --- clustering metrics ------------------------------------------------------


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


# --- reachability + shortest path (rescued from former dead-island modules) --


def shortest_path_dijkstra(g, source):
    """Level-sweeping shortest distances from ``source`` for unit-weight edges.

    A fast alternative to ``nx.shortest_path_length`` on unweighted graphs.
    Rescued from former ``graphs/dijkstra.py``.
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


def reachable_nodes_bfs(g, start):
    """Every node reachable from ``start`` via a level-order BFS. O(n + m).

    Rescued from former ``graphs/path_bfs.py``.
    """
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


def reachable_nodes(g, start, directed=False):
    """Depth-first set of nodes reachable from ``start`` (optionally directed).

    Rescued from former ``graphs/metric_connection.py``.
    """
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


def reachable_nodes_precheck(g, start):
    """DFS reachable set that filters already-seen neighbours before extending.

    A constant-factor speedup over :func:`reachable_nodes`. Rescued from
    former ``graphs/metric_complexity.py``.
    """
    seen = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            neighbors = set(g[node]) - seen
            stack.extend(neighbors)
    return seen


def is_connected(g):
    """True when every node is reachable from the first node (undirected)."""
    start = next(iter(g))
    return len(reachable_nodes(g, start)) == len(g)


def is_connected_digraph(g):
    """True when the digraph is strongly connected (every start reaches all)."""
    return all(len(reachable_nodes(g, start, directed=True)) >= len(g) for start in g)


def prob_connected(n, p, iters, rng):
    """Fraction of ``iters`` fresh G(n, p) draws that are connected.

    Corrected rescue of the old ``prob_connected(g, iters)`` which re-tested the
    same ``g`` and so always returned 1.0 or 0.0.
    """
    hits = 0
    for _ in range(iters):
        g = make_random_graph(n, p, rng)
        if is_connected(g):
            hits += 1
    return hits / iters


# --- Monte-Carlo sampled path length (rescued from graph_ws_model) -----------


def make_random_graph(n, p, rng):
    """Erdős–Rényi G(n, p): ``n`` nodes, every edge present with prob ``p``."""
    g = nx.Graph()
    nodes = range(n)
    g.add_nodes_from(nodes)
    for edge in all_pairs_undirected(nodes):
        if rng.random() < p:
            g.add_edge(*edge)
    return g


def sample_path_lengths(g, rng, trials=1000):
    """Shortest-path lengths for ``trials`` random node pairs (seeded ``rng``).

    Rescued from former ``graphs/graph_ws_model.py``. Precomputes one BFS
    distance map per source, then samples pairs and filters out self-pairs and
    unreachable pairs (dict membership instead of try/except).
    """
    nodes = list(g)
    if len(nodes) < 2:
        return []
    dist = {src: dict(nx.single_source_shortest_path_length(g, src)) for src in nodes}
    lengths = []
    for pair in rng.choice(nodes, (trials, 2)):
        u, v = int(pair[0]), int(pair[1])
        if u != v and v in dist[u]:
            lengths.append(dist[u][v])
    return lengths


def estimate_path_length(g, rng, trials=1000):
    """Mean of :func:`sample_path_lengths` -- a cheap characteristic path length."""
    ls = sample_path_lengths(g, rng, trials)
    return np.mean(ls) if ls else np.nan
