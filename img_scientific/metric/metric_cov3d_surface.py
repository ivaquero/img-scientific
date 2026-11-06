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


def plot_cov3d_surface(ax, mean, cov, grid=40):
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

    zs = np.array(
        [
            100.0 * multinorm.pdf(np.array([x, y]))
            for x, y in zip(np.ravel(xv), np.ravel(yv), strict=True)
        ]
    )
    zv = zs.reshape(xv.shape)

    ax.plot_surface(xv, yv, zv, rstride=1, cstride=1, cmap=cm.autumn)


@chart("metric/cov3d_surface")
def make_cov3d_surface(
    *,
    mean=(2.0, 17.0),
    cov=((10.0, 0.0), (0.0, 4.0)),
    grid=40,
    title="3D Gaussian PDF Surface",
):
    """The 100x bivariate-normal PDF rendered as a 3D surface."""
    set_style()

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    plot_cov3d_surface(
        ax, list(mean), np.array([list(r) for r in cov], dtype=float), grid=grid
    )
    ax.set(xlabel="X", ylabel="Y", title=title)
    return fig
