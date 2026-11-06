"""Undirected pair enumeration + G(n, p) random graph helper and chart."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style


def all_pairs_undirected(nodes):
    """Yield each unordered pair ``(u, v)`` exactly once (``i < j``)."""
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i < j:
                yield u, v


def random_pairs_undirected(nodes, p, rng):
    """Keep each undirected pair independently with probability ``p``."""
    for edge in all_pairs_undirected(nodes):
        if rng.random() < p:
            yield edge


def make_random_graph(n, p, rng):
    """Erdős–Rényi G(n, p): ``n`` nodes, every edge present with prob ``p``."""
    g = nx.Graph()
    nodes = range(n)
    g.add_nodes_from(nodes)
    g.add_edges_from(random_pairs_undirected(nodes, p, rng))
    return g


@chart("graphs/random_graph")
def make_graph_random(
    *, n=10, p=0.3, seed=42, node_color="C3", node_size=1000, title="Erdős–Rényi G(n, p)"
):
    """Circular layout of an Erdős–Rényi G(n, p) random graph."""
    set_style()

    rng = np.random.default_rng(seed)
    g = make_random_graph(n, p, rng)

    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw_circular(g, ax=ax, node_color=node_color, node_size=node_size, with_labels=True)
    ax.set(title=title)
    return fig
