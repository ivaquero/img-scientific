"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from .._registry import chart
from .._style import set_style


@chart("distrib/nbinom_pmf")
def make_nbinom_pmf(
    *,
    ns=(10, 20, 20, 40),
    ps=(0.8, 0.4, 0.8, 0.8),
    alphas=(0.2, 0.4, 0.6, 0.8),
    x_start=0,
    x_stop=26,
    x_step=1,
    title="Negative Binomial Distribution",
):
    """Bar chart of the analytic negative binomial PMF for several parameter sets."""
    set_style()

    X = np.arange(x_start, x_stop, x_step)
    fig, ax = plt.subplots()

    for n, p, alpha in zip(ns, ps, alphas, strict=True):
        y = stats.nbinom(n=n, p=p).pmf(X)
        ax.bar(X, y, label=f"n={n}, p={p}", alpha=alpha)

    ax.set(xlabel="X", ylabel="PMF(X)", title=title)
    ax.legend()
    return fig
