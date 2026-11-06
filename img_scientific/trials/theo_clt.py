"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("trials/clt")
def make_clt(
    *,
    n_sim=10000,
    ns=(12, 32, 256),
    bins=20,
    colors=("blue", "green", "orange"),
    alphas=(0.4, 0.4, 0.6),
    loc=1,
    seed=42,
    title="Central Limit Theorem",
):
    """Sampling distribution of the mean of ``n`` exponentials, for growing ``n``."""
    set_style()

    rng = np.random.default_rng(seed)

    fig, axes = plt.subplots(
        1, len(ns), figsize=(4 * len(ns), 4), constrained_layout=True, sharey=True
    )

    for ax, n, color, alpha in zip(axes, ns, colors, alphas, strict=True):
        x = stats.expon.rvs(loc=loc, size=n_sim * n, random_state=rng).reshape(
            (n_sim, n)
        )
        x_bar = x.mean(axis=1)

        ax.hist(x_bar, bins=bins, color=color, alpha=alpha)
        ax.set(
            xlim=[1.25, 3.25], title=f"{n} draws from Expo({loc})", xlabel=r"$\bar{X}$"
        )

    axes[0].set(ylabel="Frequency")
    return fig
