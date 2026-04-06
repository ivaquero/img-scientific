"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

dfs = [1, 10, 100]
alphas = [0.2, 0.2, 0.4]
colors = ["blue", "green", "orange"]

X = np.linspace(-10, 10, 100)

_, ax = plt.subplots()

for df, color, alpha in zip(dfs, colors, alphas, strict=True):
    y = stats.t.pdf(X, df=df)
    ax.plot(X, y, label=f"n={df}", color=color, alpha=alpha)
    ax.fill_between(X, y, color=color, alpha=0.25)

ax.set(xlabel="X", ylabel="PDF(X)", title="$t$ Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
