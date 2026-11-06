"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/beta_cdf")
def make_beta_cdf(
    *,
    a_params=(0.5, 1, 3),
    b_params=(0.8, 1, 3.5),
    alphas=(0.2, 0.4, 0.6),
    x_min=0,
    x_max=1,
    x_num=100,
    title="Beta Distribution",
):
    """CDF curves of the beta distribution for several ``(a, b)`` pairs."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for a, b, alpha in zip(a_params, b_params, alphas, strict=True):
        y = stats.beta(a, b).cdf(X)
        ax.plot(X, y, label=f"a = {a:2.1f}, b = {b:2.1f}", alpha=alpha)
        ax.fill_between(X, y, alpha=0.25)

    ax.set(xlabel="X", ylabel="CDF(X)", title=title)
    ax.legend()
    return fig
