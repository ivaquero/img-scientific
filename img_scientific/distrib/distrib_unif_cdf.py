"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/unif_cdf")
def make_unif_cdf(
    *,
    locs=(0, 0, 1, -1),
    scales=(1, 2, 2, 2),
    alphas=(0.4, 0.4, 0.6, 0.6),
    x_min=-4,
    x_max=4,
    x_num=100,
    title="Uniform Distribution",
):
    """CDF curves of the uniform distribution for several ``(loc, scale)`` pairs."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for loc, scale, alpha in zip(locs, scales, alphas, strict=True):
        y = stats.uniform(loc=loc, scale=scale).cdf(X)
        ax.plot(X, y, label=f"loc={loc}, scale={scale}", alpha=alpha)
        # ax.fill_between(X, y, alpha=0.25)

    ax.set(xlabel="X", ylabel="CDF(X)", title=title)
    ax.legend()
    return fig
