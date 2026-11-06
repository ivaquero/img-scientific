"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("metric/sem")
def make_sem(
    *,
    size=100,
    mean_shift=5.0,
    seed=42,
    title="Standard Deviation vs. Standard Error of the Mean",
):
    """A sample with its ±SD and ±SEM bands, mean and explanatory arrows."""
    set_style()

    rng = np.random.default_rng(seed)
    x = rng.normal(size=size) + mean_shift

    std = np.std(x, ddof=1)
    sem = stats.sem(x)

    sd = np.mean(x) + std * np.r_[-1, 1]
    se = np.mean(x) + sem * np.r_[-1, 1]

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.plot(x, ".", linestyle="None")
    ax.axhline(np.mean(x), color="orange")
    ax.axhline(sd[0], ls="--")
    ax.axhline(sd[1], ls="--")

    dashes = [20, 5]
    ax.axhline(se[0], ls="--", color="r").set_dashes(dashes)
    ax.axhline(se[1], ls="--", color="r").set_dashes(dashes)

    arrow = {
        "width": 0.25,
        "length_includes_head": True,
        "head_length": 0.2,
        "head_width": 1,
        "color": "k",
    }

    ax.arrow(10, np.mean(x), 0, std, **arrow)
    ax.arrow(10, np.mean(x), 0, -std, **arrow)
    ax.arrow(35, np.mean(x) - 5 * sem, 0, 4 * sem, **arrow)
    ax.arrow(35, np.mean(x) + 5 * sem, 0, -4 * sem, **arrow)

    ax.text(10, 5.5, " ± SD", fontsize="medium")
    ax.text(35, 5.2, " ± SEM", fontsize="medium")
    ax.annotate(
        text="mean",
        xy=(70, np.mean(x)),
        xycoords="data",
        fontsize="medium",
        xytext=(75, 5.5),
        textcoords="data",
        arrowprops={"facecolor": "black", "shrink": 0.05},
    )

    ax.set(xlabel="observation", ylabel="value", title=title)
    return fig
