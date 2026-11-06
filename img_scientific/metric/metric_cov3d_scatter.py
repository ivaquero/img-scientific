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


def plot_cov3d_scatter(ax, mean, cov):
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
    count = 1000
    x, y = multinorm.rvs(size=count).T

    zs = np.array(
        [
            100.0 * multinorm.pdf(np.array([xx, yy]))
            for xx, yy in zip(np.ravel(xv), np.ravel(yv), strict=True)
        ]
    )
    zv = zs.reshape(xv.shape)

    ax.scatter(x, y, [0] * count, marker=".")

    x = mean[0]
    zs = np.array(
        [
            100.0 * multinorm.pdf(np.array([x, y]))
            for _, y in zip(np.ravel(xv), np.ravel(yv), strict=True)
        ]
    )
    zv = zs.reshape(xv.shape)
    ax.contour(xv, yv, zv, zdir="x", offset=minx - 1, cmap=cm.binary)

    y = mean[1]
    zs = np.array(
        [
            100.0 * multinorm.pdf(np.array([x, y]))
            for x, _ in zip(np.ravel(xv), np.ravel(yv), strict=True)
        ]
    )
    zv = zs.reshape(xv.shape)
    ax.contour(xv, yv, zv, zdir="y", offset=maxy, cmap=cm.binary)


mu = [2.0, 7.0]
P = [[8.0, 0.0], [0.0, 3.0]]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
plot_cov3d_scatter(ax, mu, P)
ax.set(xlabel="X", ylabel="Y")

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/funcs/{filename}.png")
plt.show()
