"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

locs = [0, 0, 1, -1]
scales = [1, 2, 2, 2]
alphas = [0.4, 0.4, 0.6, 0.6]

X = np.linspace(-4, 4, 100)

_, ax = plt.subplots()

for loc, scale, alpha in zip(locs, scales, alphas, strict=True):
    y = stats.uniform(loc=loc, scale=scale).pdf(X)
    ax.plot(X, y, label=f"loc={loc}, scale={scale}", alpha=alpha)
    ax.fill_between(X, y, alpha=0.25)

ax.set(xlabel="X", ylabel="PDF(X)", title="Uniform Distribution")
ax.legend(loc="upper left")


filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
