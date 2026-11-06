"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt

from img_scientific._registry import chart
from img_scientific._style import set_style

from .metric_cov_ellipse import plot_cov_ellipse
from .metric_utils import multi_gaussian_product


@chart("metric/cov_prod")
def make_cov_prod(
    *,
    mean=(10, 10),
    cov_prior=((6, 0), (0, 6)),
    cov_likelihood=((2, 1.9), (1.9, 2)),
    title="Bayesian Gaussian Product",
):
    """Posterior = prior x likelihood for two Gaussians (ellipse overlays)."""
    set_style()

    c_prior = [list(r) for r in cov_prior]
    c_lik = [list(r) for r in cov_likelihood]
    c_post = multi_gaussian_product(list(mean), c_prior, list(mean), c_lik)[1]

    fig, ax = plt.subplots(figsize=(6, 4))
    plot_cov_ellipse(
        ax,
        list(mean),
        c_prior,
        edgecolor="k",
        facecolor="yellow",
        alpha=0.2,
        label="prior",
    )
    plot_cov_ellipse(
        ax,
        list(mean),
        c_lik,
        edgecolor="k",
        facecolor="green",
        alpha=0.5,
        label="likelihood",
    )
    plot_cov_ellipse(
        ax,
        list(mean),
        c_post,
        edgecolor="k",
        facecolor="navy",
        alpha=0.8,
        label="posterior",
    )
    ax.set(xlabel="x", ylabel="y", title=title)
    ax.legend()
    return fig
