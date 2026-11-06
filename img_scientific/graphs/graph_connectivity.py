"""Empirical probability a ``G(n, p)`` is connected vs ``p`` (phase transition).

Rescued visualisation for the former ``graphs/metric_connection.py`` helper.
For each ``p`` in ``ps``, we redraw ``iters`` fresh graphs and report the
fraction that pass :func:`._helpers.is_connected`.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import prob_connected


@chart("graphs/connectivity")
def make_graph_connectivity(
    *,
    n=15,
    iters=200,
    seed=42,
    ps=(0.02, 0.06, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50),
    title="P(connected) for G(n, p)",
):
    """Classic sharp transition around the connectivity threshold ``p = ln n / n``."""
    set_style()

    rng = np.random.default_rng(seed)
    probs = [prob_connected(n, p, iters, rng) for p in ps]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ps, probs, "o-", label=f"empirical (n={n}, iters={iters})")
    threshold = float(np.log(n) / n)
    ax.axvline(threshold, ls="--", lw=1, color="tab:red", label=fr"$p=\ln n/n\approx {threshold:.3f}$")
    ax.set(
        xlabel="edge probability p",
        ylabel="fraction connected",
        ylim=(-0.05, 1.05),
        title=title,
    )
    ax.legend()
    return fig
