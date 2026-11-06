"""Sierpinski triangle gasket (turtle geometry replayed with matplotlib patches)."""

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from img_scientific._registry import chart
from img_scientific._style import set_style

from ._geom import sierpinski_triangles


@chart("fractals/sierpinski_triangle")
def make_sierpinski_triangle(
    *,
    points=((-100, -50), (0, 100), (100, -50)),
    level=3,
    colormap=("blue", "red", "green", "white", "yellow", "violet", "orange"),
    edgecolor="black",
    title="Sierpinski Triangles",
):
    """Recursive filled triangles, one colour per recursion depth."""
    set_style()

    acc = []
    sierpinski_triangles([list(p) for p in points], level, acc)

    fig, ax = plt.subplots(figsize=(6, 6))
    for tri, lvl in acc:
        ax.add_patch(
            Polygon(
                tri,
                closed=True,
                facecolor=colormap[lvl],
                edgecolor=edgecolor,
                linewidth=0.3,
            )
        )

    ax.autoscale()
    ax.set(title=title)
    ax.axis("equal")
    ax.axis("off")
    return fig
