"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/gamma_pdf")
def make_gamma_pdf(
    *,
    a_params=(5, 0.5, 1),
    scale_params=(0.5, 2, 5),
    alphas=(0.4, 0.4, 0.6),
    x_min=0,
    x_max=10,
    x_num=100,
    title="Gamma Distribution",
):
    """PDF curves of the gamma distribution for several ``(a, scale)`` pairs."""
    set_style()

    X = np.linspace(x_min, x_max, x_num)
    fig, ax = plt.subplots()

    for a, lam, alpha in zip(a_params, scale_params, alphas, strict=True):
        y = stats.gamma.pdf(X, a=a, scale=lam)
        ax.plot(X, y, label=f"a = {a:.1f}, λ = {lam:.1f}", alpha=alpha)
        ax.fill_between(X, y, alpha=0.25)

    ax.set(xlabel="X", ylabel="PDF(X)", title=title)
    ax.legend()
    return fig
