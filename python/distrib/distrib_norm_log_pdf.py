"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

x = np.logspace(-9, 1, 1001) + 1e-9
func = stats.lognorm(2)
y = func.pdf(x)

_, axes = plt.subplots(1, 2, figsize=(8, 6), sharey=True, constrained_layout=True)

axes[0].plot(x, y)
axes[0].set(xlim=(-0.5, 6), xlabel="X", ylabel="PDF(X)")

axes[1].plot(np.log(x), y)
axes[1].set(xlabel="log(X)")
filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/distrs/{filename}.png")
plt.show()
