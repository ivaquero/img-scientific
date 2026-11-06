"""Turtle-free geometry shared by the fractal charts.

The original scripts drove a ``turtle`` window (no matplotlib figure). These
helpers replay the same recursive turtle command sequences as plain coordinate
lists so the charts can be drawn with matplotlib (and mirrored in Makie).
``heading`` is in degrees; ``0`` points east, positive turns counter-clockwise
(``turtle.left``), matching the turtle screen's y-up coordinate frame.
"""

import math


def koch_cmds(size, n):
    """Turtle command sequence for a Koch curve of order ``n``."""
    if n == 0:
        return [("move", size)]
    cmds = []
    for angle in (0, 60, -120, 60):
        cmds.append(("turn", angle))
        cmds.extend(koch_cmds(size / 3, n - 1))
    return cmds


def walk(cmds, start, heading=0.0):
    """Trace turtle ``cmds`` from ``start``, returning the visited ``(x, y)`` path."""
    x, y = start
    h = heading
    pts = [(x, y)]
    for kind, val in cmds:
        if kind == "turn":
            h = (h + val) % 360
        else:
            r = math.radians(h)
            x += val * math.cos(r)
            y += val * math.sin(r)
            pts.append((x, y))
    return pts


def snowflake_cmds(size, n):
    """Three Koch sides closing into the snowflake."""
    cmds = []
    for _ in range(3):
        cmds.extend(koch_cmds(size, n))
        cmds.append(("turn", -120))  # turtle.right(120)
    return cmds


def sierpinski_squares(x, y, length, level, acc):
    """Collect ``(lower-left x, y, side, level)`` squares of the fractal."""
    acc.append((x, y, length, level))
    if level == 0:
        return
    sierpinski_squares(x + length, y, length / 2, level - 1, acc)
    sierpinski_squares(x + length, y + length, length / 2, level - 1, acc)
    sierpinski_squares(x, y + length, length / 2, level - 1, acc)


def _mid(p, q):
    return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)


def sierpinski_triangles(points, level, acc):
    """Collect ``(three vertices, level)`` triangles of the gasket."""
    acc.append((points, level))
    if level == 0:
        return
    m01 = _mid(points[0], points[1])
    m02 = _mid(points[0], points[2])
    m12 = _mid(points[1], points[2])
    sierpinski_triangles([points[0], m01, m02], level - 1, acc)
    sierpinski_triangles([points[1], m01, m12], level - 1, acc)
    sierpinski_triangles([points[2], m12, m02], level - 1, acc)
