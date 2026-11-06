"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("distrib/norm3d")
def make_norm3d(
    *,
    xs=((1.0, 0.0), (2.0, 1.0), (2.0, 1.0), (5.0, 1.0)),
    ps=(
        ((1.0, 0.5), (0.5, 1.0)),
        ((1.0, 0.5), (0.5, 1.0)),
        ((1.0, 0.5), (0.5, 1.0)),
        ((1.0, 0.5), (0.5, 1.0)),
    ),
    x_range=(-5, 25),
    y_range=(-5, 5),
    n=75,
    elev=40.0,
    azim=230,
    title="3D Normal Distribution",
):
    """3D surface of summed multivariate normal PDFs."""
    set_style()

    xs = np.asarray(xs)
    ps = np.asarray(ps)

    x = np.linspace(x_range[0], x_range[1], n)
    y = np.linspace(y_range[0], y_range[1], n)
    xx, yy = np.meshgrid(x, y)
    zv = np.zeros((n, n))

    for mean, cov in zip(xs, ps, strict=True):
        multinorm = stats.multivariate_normal(mean, cov)
        zs = np.array(
            [
                multinorm.pdf(np.array([i, j]))
                for i, j in zip(np.ravel(xx), np.ravel(yy), strict=True)
            ]
        )
        zv += zs.reshape(xx.shape)

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.plot_surface(
        xx,
        yy,
        zv,
        rstride=1,
        cstride=1,
        lw=0.5,
        edgecolors="#191919",
        antialiased=True,
        shade=True,
        cmap=cm.autumn,
    )
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(title)
    return fig
