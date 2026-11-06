"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from .._registry import chart
from .._style import set_style


@chart("distrib/norm_multi_pdf")
def make_norm_multi_pdf(
    *,
    sigma_x1=1,
    sigma_x2s=(1, 2),
    rhos=(-0.9, -0.5, 0.0, 0.5, 0.9),
    xlim=(-8, 8),
    ylim=(-8, 8),
    yticks=(-5, 0, 5),
    figsize=(8, 6),
    title="Multivariate Normal Distribution",
):
    """Contour grid of bivariate normal PDFs over sigma and correlation values."""
    set_style()

    k, g = np.mgrid[-5:5:0.1, -5:5:0.1]

    pos = np.empty((*k.shape, 2))
    pos[:, :, 0], pos[:, :, 1] = k, g

    fig, ax = plt.subplots(
        len(sigma_x2s),
        len(rhos),
        sharex=True,
        sharey=True,
        figsize=figsize,
        constrained_layout=True,
    )

    for i, j in product(range(len(sigma_x2s)), range(len(rhos))):
        sigma_x2 = sigma_x2s[i]
        rho = rhos[j]
        cov = [
            [sigma_x1**2, sigma_x1 * sigma_x2 * rho],
            [sigma_x1 * sigma_x2 * rho, sigma_x2**2],
        ]
        rv = stats.multivariate_normal([0, 0], cov)
        ax[i, j].contour(k, g, rv.pdf(pos))
        ax[i, j].set(xlim=xlim, ylim=ylim, yticks=yticks)
        ax[i, j].plot(
            0, 0, label=f"$σ_{{x2}}$= {sigma_x2:3.2f} \n$ρ$= {rho:3.2f}", alpha=0
        )
        ax[i, j].legend()

    fig.text(0.5, -0.05, "x_1", ha="center")
    fig.text(-0.05, 0.5, "x_2", va="center", rotation=0)
    fig.suptitle(title)
    return fig
