"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from .._registry import chart
from .._style import set_style


@chart("distrib/weibull_pdf")
def make_weibull_pdf(
    *,
    ks=(0.5, 1, 5),
    x_start=0,
    x_stop=2.5,
    x_step=0.01,
    title="Weibull Distribution",
):
    """Line plot of the analytic Weibull (minimum) PDF for several ``c`` values."""
    set_style()

    x = np.arange(x_start, x_stop, x_step)
    fig, ax = plt.subplots()

    for k in ks:
        y = stats.weibull_min(c=k)
        ax.plot(x, y.pdf(x), label=f"k = {k:0.1f}")

    ax.set(xlabel="X", ylabel="PDF(X)", title=title)
    ax.legend()
    return fig
