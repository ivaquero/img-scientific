"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


class Gaussian(NamedTuple):
    mean: float
    var: float

    def __repr__(self):
        return f"N(μ={self.mean:.3f}, σ²={self.var**2:.3f})"


def gaussian_product(g1: Gaussian, g2: Gaussian) -> Gaussian:
    mean = (g1.var * g2.mean + g2.var * g1.mean) / (g1.var + g2.var)
    variance = (g1.var * g2.var) / (g1.var + g2.var)
    return Gaussian(mean, variance)


def plot_gaussian_product(ax, xs, g1: Gaussian, g2: Gaussian):
    g_product = gaussian_product(g1, g2)

    for g, ls in zip([g1, g2, g_product], ["-", "-", "--"], strict=True):
        ys = [stats.norm(g.mean, g.var**0.5).pdf(x) for x in xs]
        ax.plot(xs, ys, linestyle=ls, label=f"$N({g.mean:.2f}, {g.var:.2f})$")

    ax.grid(True)
    ax.legend()


@chart("trials/prod_gaussian")
def make_prod_gaussian(
    *,
    mean_1=1.0,
    var_1=10.0,
    mean_2=5.0,
    var_2=5.0,
    x_min=-15.0,
    x_max=15.0,
    x_num=100,
    title="Product of Two Gaussians",
):
    """Two Gaussians and (up to a constant) their product ``N(m1,v1)·N(m2,v2)``."""
    set_style()

    fig, ax = plt.subplots()
    xs = np.linspace(x_min, x_max, x_num)
    plot_gaussian_product(ax, xs, Gaussian(mean_1, var_1), Gaussian(mean_2, var_2))
    ax.set(title=title)
    return fig
