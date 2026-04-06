"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path
from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


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


_, ax = plt.subplots()
g1 = Gaussian(1, 10)
g2 = Gaussian(5, 5)
xs = np.linspace(-15, 15, 100)
plot_gaussian_product(ax, xs, g1, g2)

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/trials/{filename}.png")
plt.show()
