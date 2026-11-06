"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

from img_scientific._registry import chart
from img_scientific._style import set_style


def covariance_ellipse(cov, deviations=1):
    U, s, _ = np.linalg.svd(cov)
    orientation = math.atan2(U[1, 0], U[0, 0])
    width_radius = deviations * math.sqrt(s[0])
    height_radius = deviations * math.sqrt(s[1])

    if height_radius > width_radius:
        raise ValueError("width_radius must be greater than height_radius")

    return (orientation, width_radius, height_radius)


def plot_cov_ellipse(
    ax,
    mean,
    cov,
    stds=None,
    show_semiaxis=False,
    show_center=True,
    angle=1,
    edgecolor="darkslateblue",
    facecolor="green",
    alpha=0.2,
    label="",
    **line_kwargs,
):
    if stds is None:
        stds = [1]
    ellipse = covariance_ellipse(cov)

    angle = np.degrees(ellipse[0])
    width = ellipse[1] * 2.0
    height = ellipse[2] * 2.0

    for sd in stds:
        e = patches.Ellipse(mean, sd * width, sd * height, angle=angle)
        ax.add_patch(e)
        e.set(
            facecolor=facecolor,
            edgecolor=edgecolor,
            alpha=alpha,
            label=label,
            **line_kwargs,
        )

    x, y = mean
    if show_center:
        ax.scatter(x, y, marker="+", color=edgecolor)
    if show_semiaxis:
        a = ellipse[0]
        h, w = height / 4, width / 4
        ax.plot(
            [x, x + h * math.cos(a + math.pi / 2)],
            [y, y + h * math.sin(a + math.pi / 2)],
        )
        ax.plot([x, x + w * math.cos(a)], [y, y + w * math.sin(a)])


@chart("metric/cov_ellipse")
def make_cov_ellipse(
    *,
    mean=(2, 7),
    cov=((2, 0), (0, 2)),
    stds=(1, 2, 3),
    edgecolor="darkslateblue",
    facecolor="green",
    alpha=0.2,
    title="Covariance Ellipse",
):
    """Covariance ellipse of a 2x2 matrix at several standard-deviation rings."""
    set_style()

    fig, ax = plt.subplots()
    plot_cov_ellipse(
        ax,
        list(mean),
        [list(r) for r in cov],
        stds=list(stds),
        edgecolor=edgecolor,
        facecolor=facecolor,
        alpha=alpha,
    )
    ax.set(xlabel="x", ylabel="y", title=title)
    return fig
