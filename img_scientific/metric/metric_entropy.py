"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("metric/entropy")
def make_entropy(
    *,
    n=10,
    p=0.75,
    x_max=10,
    rvs_size=200,
    seed=42,
    title="Discrete Entropy (empirical vs. true vs. uniform)",
):
    """Entropy of an empirical sample, the true binomial PMF and a uniform PMF."""
    set_style()

    rng = np.random.default_rng(seed)
    x = range(x_max)
    q = stats.binom(n, p)
    r = stats.randint(0, x_max)

    draws = list(q.rvs(rvs_size, random_state=rng))
    true_distribution = [draws.count(i) / rvs_size for i in x]

    q_pmf = q.pmf(x)
    r_pmf = r.pmf(x)

    fig, axes = plt.subplots(
        1, 3, figsize=(12, 4), sharey=True, constrained_layout=True
    )

    for dist, label, ax in zip(
        [true_distribution, q_pmf, r_pmf],
        ["true_distribution", "q", "r"],
        axes.flatten(),
        strict=True,
    ):
        ax.vlines(x, 0, dist, label=f"entropy = {stats.entropy(dist):.2f}")
        ax.set_title(label)
        ax.set_xticks(x)
        ax.legend(loc=2, handlelength=0)
    fig.suptitle(title)
    return fig
