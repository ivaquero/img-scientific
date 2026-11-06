"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

αs = [5, 1 / 2, 1]
λs = [1 / 2, 2, 5]
alphas = [0.4, 0.4, 0.6]

X = np.linspace(0, 10, 100)

_, ax = plt.subplots()

for α, λ, alpha in zip(αs, λs, alphas, strict=True):
    y = stats.gamma.pdf(X, a=α, scale=λ)
    ax.plot(X, y, label=f"a = {α:.1f}, λ = {λ:.1f}", alpha=alpha)
    ax.fill_between(X, y, alpha=0.25)

ax.set(xlabel="X", ylabel="PDF(X)", title="Gamma Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
