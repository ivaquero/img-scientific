"""Logit and odds plotted against probability ``p``.

Reproduces the drawing code for the removed ``images/funcs/logit-odds.png``
reference image. Left axis is ``logit(p) = log(p / (1 - p))``; right axis is
``odds(p) = p / (1 - p)`` on a log scale. The two curves are the same
quantity under a monotone transform, and the vertical line at ``p = 0.5``
marks where both equal their neutral value (``0`` and ``1`` respectively).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("funcs/logit_odds")
def make_func_logit_odds(
    *,
    p_min=0.01,
    p_max=0.99,
    p_num=201,
    logit_color="blue",
    odds_color="red",
    title="Logit and Odds vs Probability",
):
    """Dual-axis view of ``logit(p)`` (linear) and ``odds(p)`` (log y-axis)."""
    set_style()

    p = np.linspace(p_min, p_max, p_num)
    odds = p / (1 - p)
    logit = np.log(odds)

    fig, ax_left = plt.subplots(figsize=(7, 4))
    ax_left.plot(p, logit, color=logit_color, label="logit(p)")
    ax_left.axhline(0, color="gray", lw=0.7)
    ax_left.axvline(0.5, color="gray", lw=0.7, ls=":")
    ax_left.set(
        xlabel="probability p",
        ylabel="logit(p)",
        xlim=(p_min, p_max),
        title=title,
    )

    ax_right = ax_left.twinx()
    ax_right.plot(p, odds, color=odds_color, ls="--", label="odds(p)")
    ax_right.set_yscale("log")
    ax_right.set_ylabel("odds(p) = p / (1 - p)")

    lines = ax_left.get_lines() + ax_right.get_lines()
    ax_left.legend(lines, [ln.get_label() for ln in lines], loc="upper left")
    return fig
