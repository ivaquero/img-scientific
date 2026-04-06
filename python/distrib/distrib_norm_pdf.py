"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

locs = [-1, 0, 0]
scales = [1, 1, 2]
colors = ["blue", "green", "orange"]
alphas = [0.4, 0.4, 0.6]

X = np.linspace(-10, 10, 100)

_, ax = plt.subplots()

for loc, scale, color, alpha in zip(locs, scales, colors, alphas, strict=True):
    y = stats.norm(loc=loc, scale=scale).pdf(X)
    ax.plot(X, y, label=f"μ={loc}, σ={scale}", color=color, alpha=alpha)
    ax.fill_between(X, y, color=color, alpha=0.25)

ax.set(xlabel="X", ylabel="PDF(X)", title="Normal Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
