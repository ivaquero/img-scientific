"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

λs = [1, 5, 10]
alphas = [0.2, 0.2, 0.6]

X = np.arange(0, 26, 1)

_, ax = plt.subplots()

for λ, alpha in zip(λs, alphas, strict=True):
    y = stats.poisson(mu=λ).pmf(X)
    ax.bar(X, y, label=f"λ={λ}", alpha=alpha)

ax.set(xlabel="X", ylabel="PMF(X)", title="Poisson Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
