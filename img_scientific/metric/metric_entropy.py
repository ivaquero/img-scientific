"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

np.random.default_rng(42)
x = range(10)
q = stats.binom(10, 0.75)
r = stats.randint(0, 10)

true_distribution = [list(q.rvs(200)).count(i) / 200 for i in x]

q_pmf = q.pmf(x)
r_pmf = r.pmf(x)

_, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True, constrained_layout=True)

for dist, label, ax in zip(
    [true_distribution, q_pmf, r_pmf],
    ["true_distribution", "q", "r"],
    axes.flatten(),
    strict=True,
):
    ax.vlines(x, 0, dist, label=f"entropy = {stats.entropy(dist):.2f}")
    ax.set_title(label)
    ax.set_xticks(x)
    ax.legend(loc=2, handlelength=0)

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/funcs/{filename}.png")
plt.show()
