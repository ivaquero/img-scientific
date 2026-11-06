"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np

from .._registry import chart
from .._style import set_style


@chart("distrib/categ_pmf")
def make_categ_pmf(*, n_trials=100, p=(0.2, 0.1, 0.7), seed=42):
    """Scatter of ``n_trials`` categorical samples for a fixed probability vector."""
    set_style()

    def categorical(p, k):
        return p[k]

    x = np.arange(n_trials)

    rng = np.random.default_rng(seed)
    y = [categorical(p, k=rng.randint(0, len(p) - 1)) for _ in range(n_trials)]

    μ, σ = np.mean(y), np.std(y)

    fig, ax = plt.subplots()
    ax.scatter(x, y, label=rf"$μ={μ:.2f},\ σ={σ:.2f}$")
    ax.legend()
    return fig
