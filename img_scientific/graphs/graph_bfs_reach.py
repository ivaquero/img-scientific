"""BFS reachable component highlighted on a sub-threshold Erdős–Rényi graph.

Rescued visualisation for the former ``graphs/path_bfs.py`` helper. The BFS
set-computation lives in :mod:`._helpers.reachable_nodes_bfs`; this chart draws
the whole ``G(n, p)`` and colours only the component containing ``start``.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import make_random_graph, reachable_nodes_bfs


@chart("graphs/bfs_reach")
def make_graph_bfs_reach(
    *,
    n=30,
    p=0.05,
    seed=7,
    start=0,
    node_size=900,
    title="BFS Reachable Component",
):
    """Circular layout of ``G(n, p)`` with the BFS-reachable set of ``start`` red."""
    set_style()

    rng = np.random.default_rng(seed)
    g = make_random_graph(n, p, rng)
    seen = reachable_nodes_bfs(g, start)
    colors = ["tab:red" if v in seen else "0.75" for v in g.nodes()]

    fig, ax = plt.subplots(figsize=(6, 6))
    pos = nx.circular_layout(g)
    nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.35)
    nx.draw_networkx_nodes(g, pos, ax=ax, node_color=colors, node_size=node_size)
    nx.draw_networkx_labels(g, pos, ax=ax)
    ax.set(title=f"{title} — |reach(start={start})| = {len(seen)}")
    ax.axis("off")
    return fig
