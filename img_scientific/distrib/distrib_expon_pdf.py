"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from .._registry import chart
from .._style import set_style


@chart("distrib/expon_pdf")
def make_expon_pdf(
    *,
    locs=(0.5, 1, 2),
    alphas=(0.4, 0.4, 0.6),
    x_min=0,
    x_max=10,
    x_num=100,
    title="Exponential Distribution",
):
    """PDF curves of the exponential distribution for several ``loc`` values."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for loc, alpha in zip(locs, alphas, strict=True):
        y = stats.expon.pdf(X, loc=loc)
        ax.plot(X, y, label=f"n={loc}", alpha=alpha)
        ax.fill_between(X, y, alpha=0.25)

    ax.set(xlabel="X", ylabel="PDF(X)", title=title)
    ax.legend()
    return fig
