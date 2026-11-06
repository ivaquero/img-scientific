"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style

from .metric_cov_ellipse import covariance_ellipse


def plot_cov3d_scatter(ax, mean, cov, count=1000, grid=40, rng=None):
    # get orientation, width, height of covariance ellipse
    o, w, h = covariance_ellipse(cov, 3)
    # rotate width and height to x, y axis
    wx = abs(w * math.cos(o) + h * math.sin(o)) * 1.2
    wy = abs(h * math.cos(o) - w * math.sin(o)) * 1.2

    # decentered
    w = max(wx, wy)
    minx = mean[0] - w
    maxx = mean[0] + w
    miny = mean[1] - w
    maxy = mean[1] + w

    xs = np.arange(minx, maxx, (maxx - minx) / grid)
    ys = np.arange(miny, maxy, (maxy - miny) / grid)
    xv, yv = np.meshgrid(xs, ys)

    multinorm = stats.multivariate_normal(mean, cov)
    x, y = multinorm.rvs(size=count, random_state=rng).T

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


@chart("metric/cov3d_scatter")
def make_cov3d_scatter(
    *,
    mean=(2.0, 7.0),
    cov=((8.0, 0.0), (0.0, 3.0)),
    count=1000,
    grid=40,
    seed=42,
    title="3D Covariance Scatter + Marginal Contours",
):
    """Scatter of a bivariate normal lifted to z=0 with projected marginal PDFs."""
    set_style()

    rng = np.random.default_rng(seed)
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    plot_cov3d_scatter(
        ax,
        list(mean),
        np.array([list(r) for r in cov], dtype=float),
        count=count,
        grid=grid,
        rng=rng,
    )
    ax.set(xlabel="X", ylabel="Y", title=title)
    return fig
