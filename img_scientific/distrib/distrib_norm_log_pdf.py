"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/norm_log_pdf")
def make_norm_log_pdf(
    *,
    x_start=-9,
    x_stop=1,
    x_num=1001,
    offset=1e-9,
    s=2,
    xlim=(-0.5, 6.0),
    figsize=(8, 6),
    title="Log-Normal Distribution",
):
    """Side-by-side log-normal PDF on linear and log-transformed x axes."""
    set_style()

    x = np.logspace(x_start, x_stop, x_num) + offset
    func = stats.lognorm(s)
    y = func.pdf(x)

    fig, axes = plt.subplots(
        1, 2, figsize=figsize, sharey=True, constrained_layout=True
    )

    axes[0].plot(x, y)
    axes[0].set(xlim=xlim, xlabel="X", ylabel="PDF(X)")

    axes[1].plot(np.log(x), y)
    axes[1].set(xlabel="log(X)")

    fig.suptitle(title)
    return fig
