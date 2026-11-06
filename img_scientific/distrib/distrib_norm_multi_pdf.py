"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from itertools import product
from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

σ_x1 = 1
σs_x2 = [1, 2]
ρs = [-0.90, -0.5, 0, 0.5, 0.90]

k, g = np.mgrid[-5:5:0.1, -5:5:0.1]

pos = np.empty((*k.shape, 2))
pos[:, :, 0], pos[:, :, 1] = k, g

f, ax = plt.subplots(
    len(σs_x2),
    len(ρs),
    sharex=True,
    sharey=True,
    figsize=(8, 6),
    constrained_layout=True,
)

for i, j in product(range(2), range(5)):
    σ_x2 = σs_x2[i]
    ρ = ρs[j]
    cov = [[σ_x1**2, σ_x1 * σ_x2 * ρ], [σ_x1 * σ_x2 * ρ, σ_x2**2]]
    rv = stats.multivariate_normal([0, 0], cov)
    ax[i, j].contour(k, g, rv.pdf(pos))
    ax[i, j].set(xlim=(-8, 8), ylim=(-8, 8), yticks=[-5, 0, 5])
    ax[i, j].plot(0, 0, label=f"$σ_{{x2}}$= {σ_x2:3.2f} \n$ρ$= {ρ:3.2f}", alpha=0)
    ax[i, j].legend()

f.text(0.5, -0.05, "x_1", ha="center")
f.text(-0.05, 0.5, "x_2", va="center", rotation=0)
filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
