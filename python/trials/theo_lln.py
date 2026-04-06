"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

np.random.default_rng(42)

n_sim = 1000
p = 1 / 2
x = stats.binom.rvs(1, p, size=n_sim)

x_bar = np.cumsum(x) / np.arange(1, n_sim + 1)

x = np.arange(1, n_sim + 1)
y = x_bar

_, ax = plt.subplots(figsize=(10, 5))

ax.plot(x, y, label=r"$\bar{X}$")
ax.hlines(p, 0, n_sim, linestyle="dotted", alpha=0.5, label=f"$p={p}$")

ax.set(
    xlim=[0, n_sim],
    xlabel="$n$: number of trials",
    yticks=[0.0, 0.5, 1.0],
    ylabel=r"$\bar{X}_n$",
    title="Visualizing the Law of Large Numbers",
)
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/trials/{filename}.png")
plt.show()
