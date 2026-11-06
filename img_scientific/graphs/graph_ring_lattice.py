"""Ring-lattice ``G(n, k)`` on a circular layout -- no rewiring.

Rescued visualisation for the former ``graphs/path_ring.py`` helper. The
``adjacent_edges`` / ``make_ring_lattice`` / ``make_watts_strogatz`` algorithm
now lives in :mod:`._helpers`; this chart shows the pure ring lattice that
``make_watts_strogatz`` starts from, so ``p`` and rewiring are not in the frame.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import make_ring_lattice


@chart("graphs/ring_lattice")
def make_graph_ring_lattice(
    *,
    n=12,
    k=4,
    node_size=900,
    node_color="C0",
    title="Ring Lattice G(n, k)",
):
    """Every node joined to its ``k/2`` neighbours on both sides of a ring."""
    set_style()

    g = make_ring_lattice(n, k)

    fig, ax = plt.subplots(figsize=(6, 6))
    pos = nx.circular_layout(g)
    nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.6)
    nx.draw_networkx_nodes(g, pos, ax=ax, node_color=node_color, node_size=node_size)
    nx.draw_networkx_labels(g, pos, ax=ax)
    ax.set(title=title)
    ax.axis("off")
    return fig
