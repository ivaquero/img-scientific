"""Component-size histogram via DFS reachability on a sub-threshold ``G(n, p)``.

Rescued visualisation for the former ``graphs/metric_complexity.py`` helper.
For each node we run :func:`._helpers.reachable_nodes_precheck` and record the
size of the component it sits in; the resulting histogram reveals the
small-cluster / giant-component structure of the graph.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import make_random_graph, reachable_nodes_precheck


@chart("graphs/cluster_size")
def make_graph_cluster_size(
    *,
    n=60,
    p=0.04,
    seed=42,
    title="Component Size via DFS Reachability",
):
    """Histogram of per-node reachable-set sizes; counts sum to ``n``."""
    set_style()

    rng = np.random.default_rng(seed)
    g = make_random_graph(n, p, rng)
    sizes = [len(reachable_nodes_precheck(g, start)) for start in g.nodes()]
    bins = np.arange(1, n + 2) - 0.5

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(sizes, bins=bins, edgecolor="black")
    ax.set(
        xlabel="reachable-set size (nodes)",
        ylabel="count",
        xlim=(0, n + 1),
        title=title,
    )
    return fig
