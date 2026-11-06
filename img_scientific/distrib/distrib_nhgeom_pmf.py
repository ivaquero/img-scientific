"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/nhgeom_pmf")
def make_nhgeom_pmf(
    *,
    Ns=(10, 20, 20, 40, 40),
    Ms=(2, 4, 4, 16, 32),
    rs=(2, 2, 4, 16, 16),
    alphas=(0.2, 0.2, 0.4, 0.6, 0.6),
    x_start=0,
    x_stop=26,
    x_step=1,
    title="Negative Hypergeomic Distribution",
):
    """Bar chart of the analytic negative hypergeometric PMF for several parameter sets."""
    set_style()

    fig, ax = plt.subplots()

    X = np.arange(x_start, x_stop, x_step)
    for N, M, r, alpha in zip(Ns, Ms, rs, alphas, strict=True):
        y = stats.nhypergeom(N, M, r).pmf(X)
        ax.bar(X, y, label=f"N={N}, M={M}, r={r}", alpha=alpha)

    ax.set(xlabel="X", ylabel="PMF(X)", title=title)
    ax.legend()
    return fig
