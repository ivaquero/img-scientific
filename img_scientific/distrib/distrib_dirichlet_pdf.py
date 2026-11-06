"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

plt.style.use("seaborn-v0_8-dark")

α_lists = [(1, 1, 1), (1, 1, 3), (2, 2, 6), (2, 2, 2)]
alphas = [0.3, 0.4, 0.5, 0.6]


def sampling(s=1, seed=42):
    rng = np.random.default_rng(seed)
    x = rng.randint(1, 100, size=(3, 1))
    return [s * (xi / sum(x)) for xi in x]


def beta_function(α):
    a1, a2, a3 = α
    return (
        special.gamma(a1)
        * special.gamma(a2)
        * special.gamma(a3)
        / special.gamma(sum(α))
    )


def dirichlet(x, α, n_trails):
    """
    :param x: list of [x[1,...,K], x[1,...,K], ...], shape is (n_trial, K)
    """
    c = 1 / beta_function(α)
    y = []
    for xn in x:
        prods = [xi ** (ai - 1) for xi, ai in zip(xn, α, strict=True)]
        y.append(np.prod(prods, initial=c))

    x = np.arange(n_trails)
    return x, y, np.mean(y), np.std(y)


_, ax = plt.subplots()
n_exp = 1200
for ls, alpha in zip(α_lists, alphas, strict=True):
    α = np.array(ls)
    x = [sampling() for _ in range(1, n_exp + 1)]
    x, y, _, _ = dirichlet(x, α, n_trails=n_exp)
    ax.plot(x, y, label=f"$α=({ls[0]}, {ls[1]}, {ls[2]})$", alpha=alpha)

ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
