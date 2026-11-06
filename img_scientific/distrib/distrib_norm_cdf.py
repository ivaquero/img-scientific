"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/norm_cdf")
def make_norm_cdf(
    *,
    locs=(-1, 0, 0),
    scales=(1, 1, 2),
    colors=("blue", "green", "orange"),
    alphas=(0.4, 0.4, 0.6),
    x_min=-10,
    x_max=10,
    x_num=100,
    title="Normal Distribution",
):
    """Overlaid normal CDF curves for several ``(loc, scale)`` pairs."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for loc, scale, color, alpha in zip(locs, scales, colors, alphas, strict=True):
        y = stats.norm(loc=loc, scale=scale).cdf(X)
        ax.plot(X, y, label=f"μ={loc}, σ={scale}", color=color, alpha=alpha)
        # ax.fill_between(X, y, color=color, alpha=0.25)

    ax.set(xlabel="X", ylabel="CDF(X)", title=title)
    ax.legend()
    return fig
