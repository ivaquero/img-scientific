"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/poisson_pmf")
def make_poisson_pmf(
    *,
    lambdas=(1, 5, 10),
    alphas=(0.2, 0.2, 0.6),
    x_start=0,
    x_stop=26,
    x_step=1,
    title="Poisson Distribution",
):
    """Bar chart of the analytic Poisson PMF for several ``lambda`` values."""
    set_style()

    X = np.arange(x_start, x_stop, x_step)
    fig, ax = plt.subplots()

    for lam, alpha in zip(lambdas, alphas, strict=True):
        y = stats.poisson(mu=lam).pmf(X)
        ax.bar(X, y, label=f"λ={lam}", alpha=alpha)

    ax.set(xlabel="X", ylabel="PMF(X)", title=title)
    ax.legend()
    return fig
