"""Koch curve (turtle geometry replayed with matplotlib)."""

import matplotlib.pyplot as plt

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._geom import koch_cmds, walk


@chart("fractals/koch_curve")
def make_koch_curve(
    *,
    size=600.0,
    n=3,
    start=(-300.0, -50.0),
    color="blue",
    linewidth=2.0,
    title="Koch Curve",
):
    """Order-``n`` Koch curve drawn from a start point heading east."""
    set_style()

    pts = walk(koch_cmds(size, n), start)
    xs, ys = zip(*pts, strict=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(xs, ys, color=color, linewidth=linewidth)
    ax.set(xlabel="x", ylabel="y", title=title)
    ax.axis("equal")
    ax.axis("off")
    return fig
