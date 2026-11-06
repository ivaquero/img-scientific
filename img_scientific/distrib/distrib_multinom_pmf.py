"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/multinom_pmf")
def make_multinom_pmf(*, n_trials_list=(20, 21, 22), title="Multinomial Distribution"):
    """Scatter of analytic multinomial coefficients for several trial counts."""
    set_style()

    def probs(n_trials, pair):
        if sum(pair) == n_trials:
            # a, b, c = pair
            return special.factorial(n_trials) / np.prod(
                [special.factorial(i) for i in pair]
            )
        return None

    def multinomial(n_trials):
        pairs = [
            pair
            for pair in combinations(range(1, n_trials + 1), 3)
            if sum(pair) == n_trials
        ]
        y = [probs(n_trials, pair) for pair in pairs]
        x = np.arange(len(y))
        return x, y

    fig, ax = plt.subplots()
    for n_trials in n_trials_list:
        x, y = multinomial(n_trials)
        ax.scatter(x, y, label=f"$trial = {n_trials}$")

    ax.set(title=title)
    ax.legend()
    return fig
