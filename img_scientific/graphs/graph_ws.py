"""Watts-Strogatz small-world rewiring row chart."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import make_watts_strogatz


@chart("graphs/ws_lattice")
def make_graph_ws(
    *,
    n=10,
    k=4,
    ps=(0.0, 0.2, 1.0),
    seed=42,
    node_color="red",
    node_size=200,
    title="Watts-Strogatz Rewiring",
):
    """One ring lattice (``p=0``) to one random graph (``p=1``) per panel."""
    set_style()

    rng = np.random.default_rng(seed)
    ps = list(ps)

    fig, axes = plt.subplots(1, len(ps), figsize=(4 * len(ps), 4), constrained_layout=True)
    axes = np.atleast_1d(axes).flatten()

    for p, ax in zip(ps, axes, strict=True):
        g = make_watts_strogatz(n, k, p, rng)
        pos = nx.circular_layout(g)
        nx.draw(
            g,
            ax=ax,
            pos=pos,
            with_labels=True,
            node_color=node_color,
            node_size=node_size,
            font_color="white",
            font_weight="bold",
        )
        ax.set(title=f"p = {p:g}")
        ax.axis("equal")

    fig.suptitle(title)
    return fig
