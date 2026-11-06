"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from .._registry import chart
from .._style import set_style


@chart("distrib/hgeom_pmf")
def make_hgeom_pmf(
    *,
    Ns=(10, 20, 20, 40, 40),
    Ms=(2, 4, 4, 16, 32),
    ms=(2, 2, 4, 16, 16),
    alphas=(0.2, 0.2, 0.4, 0.6, 0.6),
    x_start=0,
    x_stop=26,
    x_step=1,
    title="Hypergeomic Distribution",
):
    """Bar chart of the analytic hypergeometric PMF for several parameter sets."""
    set_style()

    fig, ax = plt.subplots()

    X = np.arange(x_start, x_stop, x_step)
    for N, M, m, alpha in zip(Ns, Ms, ms, alphas, strict=True):
        y = stats.hypergeom(N, M, m).pmf(X)
        ax.bar(X, y, label=f"N={N}, M={M}, m={m}", alpha=alpha)

    ax.set(xlabel="X", ylabel="PMF(X)", title=title)
    ax.legend()
    return fig
