"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

αs = np.array([0.5, 1, 3])
βs = np.array([0.8, 1, 3.5])
alphas = np.arange(1, len(αs) + 1) * 0.2

X = np.linspace(0, 1, 100)

_, ax = plt.subplots()

for α, β, alpha in zip(αs, βs, alphas, strict=True):
    y = stats.beta(α, β).cdf(X)
    ax.plot(X, y, label=f"a = {α:2.1f}, b = {β:2.1f}", alpha=alpha)
    ax.fill_between(X, y, alpha=0.25)

ax.set(xlabel="X", ylabel="CDF(X)", title="Beta Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
