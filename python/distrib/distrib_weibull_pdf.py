"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

x = np.arange(0, 2.5, 0.01)
ks = [0.5, 1, 5]

_, ax = plt.subplots()

for k in ks:
    y = stats.weibull_min(c=k)
    ax.plot(x, y.pdf(x), label=f"k = {k:0.1f}")

ax.set(xlabel="X", ylabel="PDF(X)", title="Weibull Distribution")
ax.legend()

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
