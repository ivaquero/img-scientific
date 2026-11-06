"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import expit as logistic

from img_scientific._registry import chart
from img_scientific._style import set_style


@chart("funcs/sigmoid")
def make_sigmoid(*, z_min=-8.0, z_max=8.0, z_num=50, color="blue", title="Sigmoid"):
    """Logistic (sigmoid) curve ``logistic(z) = 1 / (1 + exp(-z))``."""
    set_style()

    z = np.linspace(z_min, z_max, z_num)
    fig, ax = plt.subplots()

    ax.plot(z, logistic(z), color=color)
    ax.set(xlabel="z", ylabel="logistic(z)", title=title)
    return fig
