"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from .._registry import chart
from .._style import set_style


@chart("distrib/f_pdf")
def make_f_pdf(
    *,
    locs=(10, 40, 40),
    loc2s=(40, 20, 40),
    alphas=(0.4, 0.4, 0.6),
    x_min=0,
    x_max=10,
    x_num=100,
    title="F Distribution",
):
    """Line and fill plot of the analytic F PDF for several ``(dfn, dfd)`` values."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for loc, loc2, alpha in zip(locs, loc2s, alphas, strict=True):
        y = stats.f.pdf(X, dfn=loc, dfd=loc2)
        ax.plot(X, y, label=f"n1={loc}, n2={loc2}", alpha=alpha)
        ax.fill_between(X, y, alpha=0.25)

    ax.set(xlabel="X", ylabel="PMF(X)", title=title)
    ax.legend()
    return fig
