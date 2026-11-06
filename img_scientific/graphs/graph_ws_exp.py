"""Small-world experiment chart: normalized clustering C(p) and path length L(p)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._helpers import (
    characteristic_path_length,
    clustering_coefficient,
    make_watts_strogatz,
)


def _run_one_graph(n, k, p, rng):
    ws = make_watts_strogatz(n, k, p, rng)
    return characteristic_path_length(ws), clustering_coefficient(ws)


def _run_experiment(ps, n, k, iters, rng):
    res = []
    for p in ps:
        trials = np.array([_run_one_graph(n, k, p, rng) for _ in range(iters)])
        res.append(trials.mean(axis=0))
    return np.array(res)


@chart("graphs/ws_experiment")
def make_graph_ws_exp(
    *,
    n=100,
    k=10,
    iters=3,
    ps=(0.0001, 0.001, 0.01, 0.1, 1.0),
    seed=42,
    title="Normalized clustering coefficient and path length",
):
    """Both metrics divided by their ring-lattice value: the small-world window."""
    set_style()

    rng = np.random.default_rng(seed)
    ps = list(ps)

    res = _run_experiment(ps, n, k, iters, rng)
    length, coeff = res[:, 0], res[:, 1]
    length = length / length[0]
    coeff = coeff / coeff[0]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ps, coeff, "s-", lw=1, label="C(p) / C(0)")
    ax.plot(ps, length, "o-", lw=1, label="L(p) / L(0)")
    ax.set(
        xlabel="Rewiring probability (p)",
        xscale="log",
        xlim=(0.00009, 1.1),
        ylim=(-0.01, 1.01),
        title=title,
    )
    ax.legend()
    return fig
