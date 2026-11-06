"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/cauchy_pdf")
def make_cauchy_pdf(
    *,
    locs=(0, 1, 2),
    colors=("blue", "green", "orange"),
    alphas=(0.2, 0.2, 0.4),
    x_min=-10,
    x_max=10,
    x_num=100,
    title="Cauchy Distribution",
):
    """PDF curves of the Cauchy distribution for several ``loc`` values."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for loc, color, alpha in zip(locs, colors, alphas, strict=True):
        y = stats.cauchy.pdf(X, loc=loc)
        ax.plot(X, y, label=f"n={loc}", color=color, alpha=alpha)
        ax.fill_between(X, y, color=color, alpha=0.25)

    ax.set(xlabel="X", ylabel="PDF(X)", title=title)
    ax.legend()
    return fig
