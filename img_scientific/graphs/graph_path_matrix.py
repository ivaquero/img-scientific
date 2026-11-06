"""All-pairs shortest-path distance matrix as a heatmap.

Rescued visualisation for the former ``graphs/path_shortest.py`` helper.
Under the hood this is the same ``nx.shortest_path_length`` iteration that
``path_lengths`` / ``characteristic_path_length`` consume; the mean ``L`` shown
in the subtitle is computed via :func:`._helpers.characteristic_path_length`.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import characteristic_path_length, make_ring_lattice


@chart("graphs/path_matrix")
def make_graph_path_matrix(
    *,
    n=12,
    k=4,
    cmap="magma",
    title="All-Pairs Shortest-Path Distances",
):
    """Heatmap of the unweighted distance matrix for the ring lattice ``G(n, k)``."""
    set_style()

    g = make_ring_lattice(n, k)
    src_map = {u: dict(vm) for u, vm in nx.shortest_path_length(g)}
    matrix = np.array([[src_map[u][v] for v in range(n)] for u in range(n)])
    mean = characteristic_path_length(g)

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matrix, cmap=cmap)
    ax.set(
        xticks=range(n),
        yticks=range(n),
        xlabel="target v",
        ylabel="source u",
        title=f"{title}\nring lattice G({n},{k}) · mean L = {float(mean):.2f}",
    )
    fig.colorbar(im, ax=ax, label="hops")
    return fig
