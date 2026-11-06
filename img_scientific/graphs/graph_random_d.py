"""Complete directed graph helper and chart."""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx

from img_scientific._registry import chart
from img_scientific._style import set_style


def all_pairs_directed(nodes):
    """Yield every ordered pair ``(u, v)`` with ``u != v`` (both directions)."""
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i != j:
                yield u, v


def make_complete_digraph(n):
    """Directed graph with an arc between every distinct ordered pair."""
    g = nx.DiGraph()
    nodes = range(n)
    g.add_nodes_from(nodes)
    g.add_edges_from(all_pairs_directed(nodes))
    return g


@chart("graphs/complete_digraph")
def make_graph_random_d(
    *, n=5, node_color="C2", node_size=1000, title="Complete Directed Graph"
):
    """Circular layout of the complete digraph on ``n`` nodes."""
    set_style()

    g = make_complete_digraph(n)

    fig, ax = plt.subplots(figsize=(6, 6))
    nx.draw_circular(g, ax=ax, node_color=node_color, node_size=node_size, with_labels=True)
    ax.set(title=title)
    return fig
