"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("trials/lln")
def make_lln(
    *,
    n_sim=1000,
    p=0.5,
    seed=42,
    yticks=(0.0, 0.5, 1.0),
    title="Visualizing the Law of Large Numbers",
):
    """Running mean of Bernoulli(p) trials converging to ``p``."""
    set_style()

    rng = np.random.default_rng(seed)
    x = stats.binom.rvs(1, p, size=n_sim, random_state=rng)
    x_bar = np.cumsum(x) / np.arange(1, n_sim + 1)

    x = np.arange(1, n_sim + 1)
    y = x_bar

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y, label=r"$\bar{X}$")
    ax.hlines(p, 0, n_sim, linestyle="dotted", alpha=0.5, label=f"$p={p}$")

    ax.set(
        xlim=[0, n_sim],
        xlabel="$n$: number of trials",
        yticks=yticks,
        ylabel=r"$\bar{X}_n$",
        title=title,
    )
    ax.legend()
    return fig
