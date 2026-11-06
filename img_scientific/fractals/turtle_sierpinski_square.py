"""Sierpinski square fractal (turtle geometry replayed with matplotlib)."""

import matplotlib.pyplot as plt

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._geom import sierpinski_squares


@chart("fractals/sierpinski_square")
def make_sierpinski_square(
    *,
    start=(-100.0, -100.0),
    length=100.0,
    level=3,
    outer_color="blue",
    inner_color="lightgray",
    title="Sierpinski Squares",
):
    """Recursive quarter-squares: the base squares in blue, ancestors in gray."""
    set_style()

    acc = []
    sierpinski_squares(start[0], start[1], length, level, acc)

    fig, ax = plt.subplots(figsize=(6, 6))
    for x, y, side, lvl in acc:
        xs = [x, x + side, x + side, x, x]
        ys = [y, y, y + side, y + side, y]
        ax.plot(xs, ys, color=outer_color if lvl == 0 else inner_color)

    ax.set(title=title)
    ax.axis("equal")
    ax.axis("off")
    return fig
