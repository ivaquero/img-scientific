"""Logit and odds plotted against probability ``p``.

Reproduces the drawing code for the removed ``images/funcs/logit-odds.png``
reference image: ``odds(p) = p / (1 - p)`` on a **linear** left axis and
``logit(p) = log(p / (1 - p))`` on a **linear** right axis, with each axis
label colored to match its curve. Because logit is the log of odds, the two
curves converge at both corners -- near ``p -> 0`` both sit at their floor
and near ``p -> 1`` both blow up -- while the logit curve rises early above
the nearly-flat odds curve in between.
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
    odds_color="blue",
    logit_color="orange",
    title="Logit and Odds vs Probability",
):
    """Odds on a linear left axis, logit on a linear right axis."""
    set_style()

    p = np.linspace(p_min, p_max, p_num)
    odds = p / (1 - p)
    logit = np.log(odds)

    fig, ax_odds = plt.subplots(figsize=(7, 4))
    ax_odds.plot(p, odds, color=odds_color)
    ax_odds.set(
        xlabel="probability",
        xlim=(p_min, p_max),
        ylabel="odds",
        ylim=(0, odds[-1]),
        title=title,
    )
    ax_odds.tick_params(axis="y", labelcolor=odds_color)

    ax_logit = ax_odds.twinx()
    ax_logit.plot(p, logit, color=logit_color)
    ax_logit.set_ylabel("logit")
    ax_logit.set_ylim(logit.min(), logit.max())
    ax_logit.tick_params(axis="y", labelcolor=logit_color)
    return fig
