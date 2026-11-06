"""Koch snowflake (turtle geometry replayed with matplotlib)."""

import matplotlib.pyplot as plt

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._geom import snowflake_cmds, walk


@chart("fractals/koch_flake")
def make_koch_flake(
    *,
    size=400.0,
    n=3,
    start=(-200.0, 100.0),
    color="blue",
    linewidth=2.0,
    title="Koch Snowflake",
):
    """Order-``n`` Koch snowflake: three Koch sides closing the flake."""
    set_style()

    pts = walk(snowflake_cmds(size, n), start)
    xs, ys = zip(*pts, strict=True)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(xs, ys, color=color, linewidth=linewidth)
    ax.set(title=title)
    ax.axis("equal")
    ax.axis("off")
    return fig
