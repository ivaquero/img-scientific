"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from .._registry import chart
from .._style import set_style


@chart("distrib/laplace_cdf")
def make_laplace_cdf(
    *,
    locs=(-1, 0, 0),
    scales=(1.5, 1, 0.5),
    colors=("blue", "green", "orange"),
    alphas=(0.4, 0.4, 0.6),
    x_min=-10,
    x_max=10,
    x_num=100,
    title="Laplace Distribution",
):
    """CDF curves of the Laplace distribution compared with a Gaussian."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for loc, scale, color, alpha in zip(locs, scales, colors, alphas, strict=True):
        y = stats.laplace(loc=loc, scale=scale).cdf(X)
        ax.plot(X, y, label=f"μ={loc}, σ={scale}", color=color, alpha=alpha)
        # ax.fill_between(X, y, color=color, alpha=0.25)

    ax.plot(X, stats.norm.cdf(X), label="Gaussian", color="red", alpha=0.8)

    ax.set(xlabel="X", ylabel="CDF(X)", title=title)
    ax.legend()
    return fig
