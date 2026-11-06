"""Erdős–Rényi G(n, p) random graph chart."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import make_random_graph


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
