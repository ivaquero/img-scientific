"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

ps = [0.1, 0.5, 0.8]
alphas = [0.2, 0.2, 0.6]

X = np.arange(0, 26, 1)

_, ax = plt.subplots()

for p, alpha in zip(ps, alphas, strict=True):
    y = stats.geom(p=p).pmf(X)
    ax.bar(X, y, label=f"p={p}", alpha=alpha)

ax.set(xlabel="X", ylabel="PMF(X)", title="Geometric Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
