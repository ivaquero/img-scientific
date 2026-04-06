"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import expit as logistic

z = np.linspace(-8, 8)

_, ax = plt.subplots()

ax.plot(z, logistic(z))
ax.set(xlabel="z", ylabel="logistic(z)")

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/funcs/{filename}.png")
plt.show()
