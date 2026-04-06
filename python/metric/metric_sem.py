"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

rng = np.random.default_rng(42)
x = rng.normal(size=100) + 5

std = np.std(x, ddof=1)
sem = stats.sem(x)

sd = np.mean(x) + std * np.r_[-1, 1]
se = np.mean(x) + sem * np.r_[-1, 1]

_, ax = plt.subplots(figsize=(6, 4))

ax.plot(x, ".")
ax.axhline(np.mean(x), color="orange")
ax.axhline(sd[0], ls="--")
ax.axhline(sd[1], ls="--")

dashes = [20, 5]
ax.axhline(se[0], ls="--", color="r").set_dashes(dashes)
ax.axhline(se[1], ls="--", color="r").set_dashes(dashes)

arrow = {
    "width": 0.25,
    "length_includes_head": True,
    "head_length": 0.2,
    "head_width": 1,
    "color": "k",
}

ax.arrow(10, np.mean(x), 0, std, **arrow)
ax.arrow(10, np.mean(x), 0, -std, **arrow)
ax.arrow(35, np.mean(x) - 5 * sem, 0, 4 * sem, **arrow)
ax.arrow(35, np.mean(x) + 5 * sem, 0, -4 * sem, **arrow)

ax.text(10, 5.5, " ± SD", fontsize="medium")
ax.text(35, 5.2, " ± SEM", fontsize="medium")
ax.annotate(
    text="mean",
    xy=(70, np.mean(x)),
    xycoords="data",
    fontsize="medium",
    xytext=(75, 5.5),
    textcoords="data",
    arrowprops={"facecolor": "black", "shrink": 0.05},
)

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/funcs/{filename}.png")
plt.show()
