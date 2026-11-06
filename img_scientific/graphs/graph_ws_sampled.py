"""Sampled characteristic path length L(p) on Watts-Strogatz small-world graphs.

Rescued visualisation for the former ``graphs/graph_ws_model.py`` helper. The
Monte-Carlo estimator now lives in :mod:`._helpers.estimate_path_length` and
does O(trials) pair-sampled lookups instead of full all-pairs BFS, giving a
cheap L(p) curve.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import estimate_path_length, make_watts_strogatz


@chart("graphs/ws_sampled")
def make_graph_ws_sampled(
    *,
    n=80,
    k=10,
    iters=3,
    trials=400,
    seed=42,
    ps=(0.001, 0.01, 0.1, 1.0),
    title="Sampled Characteristic Path Length L(p)",
):
    """Monte-Carlo mean of pair-sampled shortest-path distances across ``p``."""
    set_style()

    rng = np.random.default_rng(seed)
    ls = []
    for pw in ps:
        vals = []
        for _ in range(iters):
            g = make_watts_strogatz(n, k, pw, rng)
            vals.append(estimate_path_length(g, rng, trials))
        ls.append(float(np.mean(vals)))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ps, ls, "o-", label=f"sampled (trials={trials}, iters={iters})")
    ax.set(
        xlabel="rewiring probability p",
        ylabel="mean path length",
        xscale="log",
        title=title,
    )
    ax.legend()
    return fig
