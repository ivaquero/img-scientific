"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")


def plot_bernoulli_pmf(ax, ps, alphas, X):
    for p, alpha in zip(ps, alphas, strict=True):
        y = stats.bernoulli(p=p).pmf(X)
        ax.bar(X, y, label=f"p={p}", alpha=alpha)

    ax.set(xlabel="X", ylabel="PMF(X)", title="Bernoulli Distribution")
    ax.legend()


ps = [0.1, 0.5, 0.8]
alphas = [0.2, 0.2, 0.6]
X = np.arange(0, 26, 1)

_, ax = plt.subplots()
plot_bernoulli_pmf(ax, ps, alphas, X)

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
