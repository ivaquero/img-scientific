"""Regular graph construction helper and circular chart."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from img_scientific._registry import chart
from img_scientific._style import set_style

from .path_ring import adjacent_edges


def opposite_edges(nodes):
    """Yield an edge from each node to its diametrically opposite ring node."""
    n = len(nodes)
    for i, u in enumerate(nodes):
        j = i + n // 2
        v = nodes[j % n]
        yield u, v


def make_regular_graph(n, k):
    """Build a ``k``-regular graph on ``n`` nodes (ring neighbours + opposites)."""
    # a is the number of adjacent edges, b is the number of opposite edges (0/1)
    a, b = divmod(k, 2)

    g = nx.Graph()
    nodes = range(n)
    g.add_nodes_from(nodes)
    g.add_edges_from(adjacent_edges(nodes, a))
    if b:
        if n % 2:
            msg = "Can not make a regular graph"
            raise ValueError(msg)
        g.add_edges_from(opposite_edges(nodes))
    return g


@chart("graphs/regular")
def make_path_regular(
    *, n=10, k=3, node_color="C4", node_size=1000, title="Regular Graph"
):
    """Circular layout of a ``k``-regular graph on ``n`` nodes."""
    set_style()

    g = make_regular_graph(n, k)

    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw_circular(g, ax=ax, node_color=node_color, node_size=node_size, with_labels=True)
    ax.set(title=title)
    return fig
