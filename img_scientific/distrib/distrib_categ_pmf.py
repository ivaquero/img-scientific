from os import path

import numpy as np
from matplotlib import pyplot as plt

plt.style.use("seaborn-v0_8-dark")


def categorical(p, k):
    return p[k]


n_trials = 100
p = [0.2, 0.1, 0.7]

x = np.arange(n_trials)

rng = np.random.default_rng(42)
y = [categorical(p, k=rng.randint(0, len(p) - 1)) for _ in range(n_trials)]

μ, σ = np.mean(y), np.std(y)

_, ax = plt.subplots()
ax.scatter(x, y, label=rf"$μ={μ:.2f},\ σ={σ:.2f}$")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
