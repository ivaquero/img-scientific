"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

Ns = [10, 20, 20, 40, 40]
Ms = [2, 4, 4, 16, 32]
ms = [2, 2, 4, 16, 16]
alphas = [0.2, 0.2, 0.4, 0.6, 0.6]

_, ax = plt.subplots()

X = np.arange(0, 26, 1)
for N, M, m, alpha in zip(Ns, Ms, ms, alphas, strict=True):
    y = stats.hypergeom(N, M, m).pmf(X)
    ax.bar(X, y, label=f"N={N}, M={M}, m={m}", alpha=alpha)

ax.set(xlabel="X", ylabel="PMF(X)", title="Hypergeomic Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
