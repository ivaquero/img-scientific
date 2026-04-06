"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

locs = [0, 1, 2]
alphas = [0.2, 0.2, 0.4]
colors = ["blue", "green", "orange"]

X = np.linspace(-10, 10, 100)

_, ax = plt.subplots()

for loc, color, alpha in zip(locs, colors, alphas, strict=True):
    y = stats.cauchy.pdf(X, loc=loc)
    ax.plot(X, y, label=f"n={loc}", color=color, alpha=alpha)
    ax.fill_between(X, y, color=color, alpha=0.25)

ax.set(xlabel="X", ylabel="PDF(X)", title="Cauchy Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
