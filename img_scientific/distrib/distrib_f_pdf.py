"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

locs = [10, 40, 40]
loc2s = [40, 20, 40]
alphas = [0.4, 0.4, 0.6]

X = np.linspace(0, 10, 100)

_, ax = plt.subplots()

for loc, loc2, alpha in zip(locs, loc2s, alphas, strict=True):
    y = stats.f.pdf(X, dfn=loc, dfd=loc2)
    ax.plot(X, y, label=f"n1={loc}, n2={loc2}", alpha=alpha)
    ax.fill_between(X, y, alpha=0.25)

ax.set(xlabel="X", ylabel="PMF(X)", title="F Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
