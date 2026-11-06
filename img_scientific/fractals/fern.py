"""Barnsley fern iterated-function-system scatter."""

import matplotlib.pyplot as plt
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style


def _t1(p):
    x, y = p
    return 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6


def _t2(p):
    x, y = p
    return 0.20 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6


def _t3(p):
    x, y = p
    return -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44


def _t4(p):
    _, y = p
    return 0.0, 0.16 * y


_TRANSFORMS = [_t1, _t2, _t3, _t4]
_PROBABILITIES = [0.85, 0.07, 0.07, 0.01]


def generate_fern(num_points, rng):
    points = [(0.0, 0.0)]
    current = np.array([0.0, 0.0])
    for _ in range(num_points):
        current = np.array(_TRANSFORMS[rng.choice(4, p=_PROBABILITIES)](current))
        points.append(tuple(current))
    return points


@chart("fractals/fern")
def make_fern(
    *, num_points=50000, seed=1, color="green", point_size=0.2, title="Barnsley Fern"
):
    """Barnsley-fern IFS: iterated affine maps chosen with fixed probabilities."""
    set_style()

    rng = np.random.default_rng(seed)
    pts = generate_fern(num_points, rng)
    xs, ys = zip(*pts, strict=True)

    fig = plt.figure(figsize=(6, 9))
    ax = fig.add_subplot()
    ax.scatter(xs, ys, s=point_size, c=color)
    ax.set(title=title)
    ax.axis("off")
    return fig
