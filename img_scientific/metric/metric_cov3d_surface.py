"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import math
from os import path

import matplotlib.pyplot as plt
import metric_cov_ellipse
import numpy as np
from matplotlib import cm
from scipy import stats


def plot_cov3d_surface(ax, mean, cov):
    # get orientation, width, height of covariance ellipse
    o, w, h = metric_cov_ellipse.covariance_ellipse(cov, 3)
    # rotate width and height to x, y axis
    wx = abs(w * math.cos(o) + h * math.sin(o)) * 1.2
    wy = abs(h * math.cos(o) - w * math.sin(o)) * 1.2

    # decentered
    w = max(wx, wy)
    minx = mean[0] - w
    maxx = mean[0] + w
    miny = mean[1] - w
    maxy = mean[1] + w

    xs = np.arange(minx, maxx, (maxx - minx) / 40.0)
    ys = np.arange(miny, maxy, (maxy - miny) / 40.0)
    xv, yv = np.meshgrid(xs, ys)

    multinorm = stats.multivariate_normal(mean, cov)

    zs = np.array(
        [
            100.0 * multinorm.pdf(np.array([x, y]))
            for x, y in zip(np.ravel(xv), np.ravel(yv), strict=True)
        ]
    )
    zv = zs.reshape(xv.shape)

    ax.plot_surface(xv, yv, zv, rstride=1, cstride=1, cmap=cm.autumn)


mean = [2.0, 17.0]
cov = [[10.0, 0.0], [0.0, 4.0]]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
plot_cov3d_surface(ax, mean, cov)
ax.set(xlabel="X", ylabel="Y")

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/funcs/{filename}.png")
plt.show()
