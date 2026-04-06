"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from itertools import combinations
from os import path

import numpy as np
from matplotlib import pyplot as plt
from scipy import special

plt.style.use("seaborn-v0_8-dark")


def probs(n_trials, pair):
    if sum(pair) == n_trials:
        # a, b, c = pair
        return special.factorial(n_trials) / np.prod(
            [special.factorial(i) for i in pair]
        )
    return None


def multinomial(n_trials):
    pairs = [
        pair
        for pair in combinations(range(1, n_trials + 1), 3)
        if sum(pair) == n_trials
    ]
    y = [probs(n_trials, pair) for pair in pairs]
    x = np.arange(len(y))
    return x, y


_, ax = plt.subplots()
for n_trials in [20, 21, 22]:
    x, y = multinomial(n_trials)
    ax.scatter(x, y, label=f"$trial = {n_trials}$")

ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
