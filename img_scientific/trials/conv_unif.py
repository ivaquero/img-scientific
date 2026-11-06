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
x = stats.uniform.rvs(size=10**5)
y = stats.uniform.rvs(size=10**5)

t = x + y

_, ax = plt.subplots()

ax.hist(t, bins=20)
ax.set(xlabel="$x + y$", ylabel="Frequency", title="Histogram of $T = X + Y$")

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/trials/{filename}.png")
plt.show()
