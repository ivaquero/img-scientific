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

n_sim = 10**4
ns = [12, 32, 256]
colors = ["blue", "green", "orange"]
alphas = [0.4, 0.4, 0.6]

fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True, sharey=True)

for ax, n, color, alpha in zip(axes, ns, colors, alphas, strict=True):
    x = stats.expon.rvs(loc=1, size=n_sim * n).reshape((n_sim, n))
    x_bar = x.mean(axis=1)

    ax.hist(x_bar, bins=20, color=color, alpha=alpha)
    ax.set(xlim=[1.25, 3.25], title=f"{n} draws from Expo(1)", xlabel=r"$\bar{X}$")

axes[0].set(ylabel="Frequency")

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/trials/{filename}.png")
plt.show()
