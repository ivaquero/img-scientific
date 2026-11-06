"""Per-node clustering coefficient as a bar chart.

Rescued visualisation for the former ``graphs/metric_clustering.py`` helper.
Bars show :func:`._helpers.node_clustering` for each node of a Watts-Strogatz
graph, and the dashed horizontal line is :func:`._helpers.clustering_coefficient`
(mean over nodes).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import clustering_coefficient, make_watts_strogatz, node_clustering


@chart("graphs/clustering_bars")
def make_graph_clustering_bars(
    *,
    n=15,
    k=4,
    p=0.2,
    seed=42,
    node_color="C1",
    title="Per-Node Clustering Coefficient",
):
    """Bar of ``C(u)`` per node, with graph-mean ``C`` overlaid as a hline."""
    set_style()

    rng = np.random.default_rng(seed)
    g = make_watts_strogatz(n, k, p, rng)
    vals = [node_clustering(g, u) for u in g.nodes()]
    mean = clustering_coefficient(g)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(range(n), vals, color=node_color, alpha=0.75, label="per-node")
    ax.axhline(mean, ls="--", color="tab:red", label=fr"$\bar{{C}} = {mean:.3f}$")
    ax.set(
        xlabel="node index",
        ylabel="clustering coefficient",
        ylim=(0, 1),
        title=title,
    )
    ax.legend(loc="upper right")
    return fig
