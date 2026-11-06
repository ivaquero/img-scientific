"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from .._registry import chart
from .._style import set_style


@chart("distrib/t_pdf")
def make_t_pdf(
    *,
    dfs=(1, 10, 100),
    alphas=(0.2, 0.2, 0.4),
    colors=("blue", "green", "orange"),
    x_min=-10,
    x_max=10,
    x_num=100,
    title="$t$ Distribution",
):
    """Line and fill plot of the analytic Student's t PDF for several ``df`` values."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for df, color, alpha in zip(dfs, colors, alphas, strict=True):
        y = stats.t.pdf(X, df=df)
        ax.plot(X, y, label=f"n={df}", color=color, alpha=alpha)
        ax.fill_between(X, y, color=color, alpha=0.25)

    ax.set(xlabel="X", ylabel="PDF(X)", title=title)
    ax.legend()
    return fig
