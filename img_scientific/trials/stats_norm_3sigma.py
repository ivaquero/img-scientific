"""
Code by Xavier Yang(@ivaquero)
https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("trials/norm_3sigma")
def make_norm_3sigma(
    *,
    loc=0.0,
    scale=1.0,
    n_sigma=3,
    colors=("red", "orange", "yellow"),
    alphas=(0.2, 0.2, 0.1),
    x_min=-3.0,
    x_max=3.0,
    x_num=100,
    y_min=0.0,
    y_max=0.45,
    title="Percentage of X falling between $i$ σ",
):
    """Normal PDF with the ``1σ/2σ/3σ`` bands shaded and their coverage labelled."""
    set_style()

    fig, ax = plt.subplots(figsize=(6, 4))

    func = stats.norm(loc, scale)
    X = np.linspace(x_min, x_max, x_num)
    y = func.pdf(X)

    ax.plot(X, y, color="r", alpha=alphas[-1])

    for i in range(n_sigma):
        start = loc - scale * (i + 1)
        end = loc + scale * (i + 1)
        y_fall = func.cdf(end) - func.cdf(start)

        X_dist = X[end >= X][X[end >= X] >= start]
        y_dist = func.pdf(X_dist)
        ax.fill_between(
            X_dist,
            y_dist,
            color=colors[i],
            alpha=alphas[i],
            label=f"i = {i + 1}, % = {round(y_fall, 3)}",
        )

    ax.set(xlim=(x_min, x_max), ylim=(y_min, y_max), title=title)
    ax.legend()
    return fig
