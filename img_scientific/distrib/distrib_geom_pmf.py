"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/geom_pmf")
def make_geom_pmf(
    *,
    ps=(0.1, 0.5, 0.8),
    alphas=(0.2, 0.2, 0.6),
    x_start=0,
    x_stop=26,
    x_step=1,
    title="Geometric Distribution",
):
    """Bar chart of the analytic geometric PMF for several ``p`` values."""
    set_style()

    X = np.arange(x_start, x_stop, x_step)
    fig, ax = plt.subplots()

    for p, alpha in zip(ps, alphas, strict=True):
        y = stats.geom(p=p).pmf(X)
        ax.bar(X, y, label=f"p={p}", alpha=alpha)

    ax.set(xlabel="X", ylabel="PMF(X)", title=title)
    ax.legend()
    return fig
