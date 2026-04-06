"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

ns = [10, 20, 20, 40]
ps = [0.2, 0.1, 0.2, 0.2]
alphas = np.arange(1, len(ns) + 1) * 0.2

X = np.arange(0, 20 + 1)

_, ax = plt.subplots()

for n, p, alpha in zip(ns, ps, alphas, strict=True):
    y = stats.binom(n=n, p=p).pmf(X)
    ax.bar(X, y, label=f"N={n}, p={p}", alpha=alpha)

ax.set(xlabel="x", ylabel="PMF(X)", title="Binomial Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
