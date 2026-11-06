"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("trials/conv_unif")
def make_conv_unif(
    *, n_trials=100000, bins=20, seed=42, color="blue", title="Histogram of $T = X + Y$"
):
    """Histogram of ``T = X + Y`` for two i.i.d. uniforms (triangular law)."""
    set_style()

    rng = np.random.default_rng(seed)
    x = stats.uniform.rvs(size=n_trials, random_state=rng)
    y = stats.uniform.rvs(size=n_trials, random_state=rng)
    t = x + y

    fig, ax = plt.subplots()
    ax.hist(t, bins=bins, color=color)
    ax.set(xlabel="$x + y$", ylabel="Frequency", title=title)
    return fig
