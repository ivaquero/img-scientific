"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import math
from os import path

import matplotlib.pyplot as plt
import numpy as np


def sort_eigval(cov, asc=True):
    eigval, eigvec = np.linalg.eigh(cov)
    order = eigval.argsort()

    return eigval[order], eigvec[:, order]


def plot_3d_covariance(ax, mean, cov, std=1.0, color=None, alpha=1.0, N=60, **kwargs):
    mean = np.atleast_2d(mean)
    if mean.shape != (1, 3):
        raise ValueError("mean must be convertible to a 1x3 row vector")
    if cov.shape != (3, 3):
        raise ValueError("covariance must be 3x3")

    mean = mean[0]
    cov = np.asarray(cov)
    eigval, eigvec = sort_eigval(cov)
    radii = std * np.sqrt(np.real(eigval))

    if eigval[0] < 0:
        raise ValueError("covariance matrix must be positive definite")

    # calculate cartesian coordinates for the ellipsoid surface
    u = np.linspace(0.0, 2.0 * math.pi, N)
    v = np.linspace(0.0, math.pi, N)
    x = np.outer(math.cos(u), math.sin(v)) * radii[0]
    y = np.outer(math.sin(u), math.sin(v)) * radii[1]
    z = np.outer(np.ones_like(u), math.cos(v)) * radii[2]

    # rotate data with eigenvector and center on mu
    a = np.kron(eigvec[:, 0], x)
    b = np.kron(eigvec[:, 1], y)
    c = np.kron(eigvec[:, 2], z)

    data = a + b + c
    N = data.shape[0]
    x = data[:, 0:N] + mean[0]
    y = data[:, N : N * 2] + mean[1]
    z = data[:, N * 2 :] + mean[2]

    ax.plot_surface(
        x, y, z, rstride=3, cstride=3, linewidth=0.1, alpha=alpha, color=color, **kwargs
    )

    r = radii.max()
    ax.set(
        xlabel="X",
        ylabel="Y",
        zlabel="Z",
        xlim=(-r + mean[0], r + mean[0]),
        ylim=(-r + mean[1], r + mean[1]),
        zlim=(-r + mean[2], r + mean[2]),
    )


mu = [0.3, 5.0, 10.0]
C = np.array([[1.0, 0.03, 0.2], [0.03, 4.0, 0.0], [0.2, 0.0, 16.1]])
rng = np.random.default_rng(42)
sample = rng.multivariate_normal(mu, C, size=1000)

fig = plt.gcf()
ax = fig.add_subplot(111, projection="3d")
plot_3d_covariance(ax, mu, C, alpha=0.4, std=3)
ax.scatter(sample[:, 0], sample[:, 1], zs=sample[:, 2])

filename, extension = path.splitext(path.basename(__file__))
# plt.savefig(f"../../images/funcs/{filename}.png")
plt.show()
