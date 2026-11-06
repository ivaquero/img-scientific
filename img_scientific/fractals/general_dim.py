"""Generalized (multifractal) dimension curves: tau(q), D_q and f(alpha)."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import comb

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("fractals/general_dim")
def make_general_dim(
    *,
    p1=1 / 9,
    p2=8 / 9,
    k=500,
    x_min=-20.0,
    x_max=20.0,
    tau_num=1000,
    dq_num=100,
    title="Generalized (Multifractal) Dimensions",
):
    """Two-bin multifractal: mass-exponent τ(q), generalized dimension D_q and
    the singularity spectrum f(α)."""
    set_style()

    log3 = np.log(3)
    log_inv3 = np.log(1 / 3)

    fig, axes = plt.subplots(3, 1, constrained_layout=True)

    # The tau curve
    xq = np.linspace(x_min, x_max, tau_num)
    tau = np.log(p1**xq + p2**xq) / log3
    axes[0].plot(xq, tau)
    axes[0].set(xlabel="$q$", ylabel=r"$τ(q)$")

    # The D_q curve
    x1 = np.linspace(x_min, 0.99, dq_num)
    x2 = np.linspace(0.99, x_max, dq_num)
    Dq1 = np.log(p1**x1 + p2**x1) / (log3 * (1 - x1))
    Dq2 = np.log(p2**x2 + p1**x2) / (log3 * (1 - x2))
    axes[1].plot(x1, Dq1, x2, Dq2)
    axes[1].set(xlabel="q", ylabel="$D_q$")

    # The f(alpha) curve
    s = np.arange(k)
    xa = (s * np.log(p1) + (k - s) * np.log(p2)) / (k * log_inv3)
    f = -(np.log(comb(k, s))) / (k * log_inv3)
    axes[2].plot(xa, f)
    axes[2].set(xlabel=r"$α$", ylabel=r"$f(α)$")

    fig.suptitle(title)
    return fig
