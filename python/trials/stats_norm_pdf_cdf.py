"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

from os import path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.style.use("seaborn-v0_8-dark")

_, axes = plt.subplots(1, 2, figsize=(8, 4))

start, end = -4, 4
loc, scale = 0, 1
func = stats.norm(loc, scale)

x = np.linspace(start, end, 201)
y = func.pdf(x)

ix = np.linspace(start, loc)
iy = func.pdf(ix)

shade = [(start, 0), *zip(ix, iy, strict=True), (loc, 0)]
polygon = plt.Polygon(shade, facecolor="0.9", edgecolor="0.5")
axes[0].plot(x, y)
axes[0].add_patch(polygon)

axes[0].text(
    0.2 * (start + loc),
    0.25 * func.pdf(loc),
    "CDF(x)",
    horizontalalignment="center",
    fontsize="small",
)
axes[0].set(xlabel="x", ylabel="PDF(x)")

y_ = func.cdf(x)
axes[1].plot(x, y_)
axes[1].plot(loc, func.cdf(loc), marker="o", color="b")

axes[1].axvline(x=0, ymin=0.05, ymax=1, ls="--")
axes[1].set(xlabel="x", ylabel="CDF(x)")

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/trials/{filename}.png")
plt.show()
