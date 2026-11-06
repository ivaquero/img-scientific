"""
Code by Xavier Yang(@ivaquero)
https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

loc, scale = 0, 1
alpha = [0.2, 0.2, 0.1]
colors = ["red", "orange", "yellow"]

_, ax = plt.subplots(figsize=(6, 4))

func = stats.norm(loc, scale)
X = np.linspace(-3, 3, 100)
y = func.pdf(X)

ax.plot(X, y, color="r", alpha=alpha[2])

for i in range(3):
    start = loc - scale * (i + 1)
    end = loc + scale * (i + 1)
    y_fall = func.cdf(end) - func.cdf(start)

    X_dist = X[end >= X][X[end >= X] >= start]
    y_dist = func.pdf(X_dist)
    ax.fill_between(
        X_dist,
        y_dist,
        color=colors[i],
        alpha=alpha[i],
        label=f"i = {i + 1}, % = {round(y_fall, 3)}",
    )

ax.set(xlim=(-3, 3), ylim=(0, 0.45), title="Percentage of X falling between $i$ σ")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/trials/{filename}.png")
plt.show()
