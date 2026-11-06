"""G(n, m) Erdos-Renyi random graph (fixed edge count) helper and chart."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from .graph_random import all_pairs_undirected


def m_pairs(nodes, m, rng):
    """Choose ``m`` distinct undirected pairs uniformly at random (seeded)."""
    pairs = list(all_pairs_undirected(nodes))
    idx = rng.choice(len(pairs), size=m, replace=False)
    return [pairs[i] for i in idx]


def make_m_graph(n, m, rng):
    """Erdős–Rényi G(n, m): ``n`` nodes and exactly ``m`` random edges."""
    g = nx.Graph()
    nodes = range(n)
    g.add_nodes_from(nodes)
    g.add_edges_from(m_pairs(nodes, m, rng))
    return g


@chart("graphs/random_nm")
def make_graph_er(
    *, n=10, m=15, seed=42, node_color="C4", node_size=1000, title="Erdős–Rényi G(n, m)"
):
    """Circular layout of an Erdős–Rényi G(n, m) random graph."""
    set_style()

    rng = np.random.default_rng(seed)
    g = make_m_graph(n, m, rng)

    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw_circular(g, ax=ax, node_color=node_color, node_size=node_size, with_labels=True)
    ax.set(title=title)
    return fig
