"""Level-sweeping shortest-path distances (Dijkstra-style) on a ring lattice.

Rescued visualisation for the former ``graphs/dijkstra.py`` helper: the algorithm
itself now lives in :mod:`._helpers.shortest_path_dijkstra`, and this file
renders it as a circular ring lattice with nodes coloured by BFS distance from
a chosen ``source``.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import make_ring_lattice, shortest_path_dijkstra


@chart("graphs/dijkstra")
def make_graph_dijkstra(
    *,
    n=15,
    k=4,
    source=0,
    node_size=900,
    cmap="viridis",
    title="Shortest-Path Levels (Dijkstra)",
):
    """Ring lattice ``G(n, k)`` with nodes coloured by shortest-hop distance."""
    set_style()

    g = make_ring_lattice(n, k)
    dist = shortest_path_dijkstra(g, source)
    colors = np.array([dist.get(v, -1) for v in g.nodes()], dtype=float)

    fig, ax = plt.subplots(figsize=(6, 6))
    pos = nx.circular_layout(g)
    sc = nx.draw_networkx_nodes(
        g, pos, ax=ax, node_color=colors, node_size=node_size, cmap=cmap
    )
    sc.set_array([])
    nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.4)
    nx.draw_networkx_labels(g, pos, ax=ax)
    fig.colorbar(sc, ax=ax, shrink=0.7, label="hops from source")
    ax.set(title=title)
    ax.axis("equal")
    return fig
