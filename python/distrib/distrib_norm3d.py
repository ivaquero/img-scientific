"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from scipy import stats

xs = np.array([[1.0, 0.0], [2.0, 1.0], [2, 1.0], [5, 1.0]])
ps = np.array(
    [
        [[1.0, 0.5], [0.5, 1.0]],
        [[1.0, 0.5], [0.5, 1.0]],
        [[1.0, 0.5], [0.5, 1.0]],
        [[1.0, 0.5], [0.5, 1.0]],
    ]
)

x_range, y_range = (-5, 25), (-5, 5)
N = 75

xs = np.asarray(xs)
x = np.linspace(x_range[0], x_range[1], N)
y = np.linspace(y_range[0], y_range[1], N)
xx, yy = np.meshgrid(x, y)
zv = np.zeros((N, N))

for mean, cov in zip(xs, ps, strict=True):
    multinorm = stats.multivariate_normal(mean, cov)
    zs = np.array(
        [
            multinorm.pdf(np.array([i, j]))
            for i, j in zip(np.ravel(xx), np.ravel(yy), strict=True)
        ]
    )
    zv += zs.reshape(xx.shape)

ax = plt.figure().add_subplot(111, projection="3d")
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
ax.view_init(elev=40.0, azim=230)
plt.show()
