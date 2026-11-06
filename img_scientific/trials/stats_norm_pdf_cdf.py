"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("trials/norm_pdf_cdf")
def make_norm_pdf_cdf(
    *, loc=0.0, scale=1.0, x_min=-4.0, x_max=4.0, x_num=201, title="Normal PDF and CDF"
):
    """Left: normal PDF with the ``[x_min, loc]`` area shaded; right: the CDF."""
    set_style()

    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    func = stats.norm(loc, scale)

    x = np.linspace(x_min, x_max, x_num)
    y = func.pdf(x)

    ix = np.linspace(x_min, loc)
    iy = func.pdf(ix)

    shade = [(x_min, 0), *zip(ix, iy, strict=True), (loc, 0)]
    polygon = plt.Polygon(shade, facecolor="0.9", edgecolor="0.5")
    axes[0].plot(x, y)
    axes[0].add_patch(polygon)

    axes[0].text(
        0.2 * (x_min + loc),
        0.25 * func.pdf(loc),
        "CDF(x)",
        horizontalalignment="center",
        fontsize="small",
    )
    axes[0].set(xlabel="x", ylabel="PDF(x)")

    y_ = func.cdf(x)
    axes[1].plot(x, y_)
    axes[1].plot(loc, func.cdf(loc), marker="o", color="b")

    axes[1].axvline(x=loc, ymin=0.05, ymax=1, ls="--")
    axes[1].set(xlabel="x", ylabel="CDF(x)")

    fig.suptitle(title)
    return fig
