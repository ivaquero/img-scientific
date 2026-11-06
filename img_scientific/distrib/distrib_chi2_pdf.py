"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/chi2_pdf")
def make_chi2_pdf(
    *,
    locs=(0.5, 1, 2.5),
    alphas=(0.4, 0.4, 0.6),
    x_min=0,
    x_max=10,
    x_num=100,
    title="$χ^2$ Distribution",
):
    """Line and fill plot of the analytic chi-squared PDF for several ``df`` values."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for loc, alpha in zip(locs, alphas, strict=True):
        y = stats.chi2.pdf(X, df=loc)
        ax.plot(X, y, label=f"n={loc}", alpha=alpha)
        ax.fill_between(X, y, alpha=0.25)

    ax.set(xlabel="X", ylabel="PDF(X)", title=title)
    ax.legend()
    return fig
