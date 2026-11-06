"""
_helpers.jl -- fractal-topic geometry shared by the turtle-replacement charts.

Mirrors ``img_scientific/fractals/_geom.py``: the original scripts drove a
``turtle`` window; here the same recursive command sequences are replayed as
plain coordinate lists so they can be drawn with Makie ``lines!`` / ``poly!``.

``heading`` is in degrees; ``0`` points east and positive turns
counter-clockwise (``turtle.left``), matching the y-up screen frame.
"""

# --- Koch turtle command sequence + walker -----------------------------------

"""Turtle command sequence for a Koch curve of order ``n`` (list of (kind, val))."""
function koch_cmds(size, n)
    n == 0 && return Tuple{Symbol, Float64}[(:move, Float64(size))]
    cmds = Tuple{Symbol, Float64}[]
    for angle in (0, 60, -120, 60)
        push!(cmds, (:turn, Float64(angle)))
        append!(cmds, koch_cmds(size / 3, n - 1))
    end
    cmds
end

"""Three Koch sides closing into the snowflake."""
function snowflake_cmds(size, n)
    cmds = Tuple{Symbol, Float64}[]
    for _ in 1:3
        append!(cmds, koch_cmds(size, n))
        push!(cmds, (:turn, -120.0))  # turtle.right(120)
    end
    cmds
end

"""Trace turtle ``cmds`` from ``start``, returning the visited ``(x, y)`` path."""
function walk(cmds, start, heading = 0.0)
    x, y = Float64(start[1]), Float64(start[2])
    h = heading
    xs, ys = Float64[x], Float64[y]
    for (kind, val) in cmds
        if kind === :turn
            h = mod(h + val, 360)
        else
            r = deg2rad(h)
            x += val * cos(r)
            y += val * sin(r)
            push!(xs, x)
            push!(ys, y)
        end
    end
    xs, ys
end

# --- Sierpinski generators (fill accumulators, like the Python versions) ------

"""Collect ``(x, y, side, level)`` lower-left squares of the fractal into ``acc``."""
function sierpinski_squares!(x, y, length, level, acc)
    push!(acc, (Float64(x), Float64(y), Float64(length), level))
    level == 0 && return acc
    sierpinski_squares!(x + length, y, length / 2, level - 1, acc)
    sierpinski_squares!(x + length, y + length, length / 2, level - 1, acc)
    sierpinski_squares!(x, y + length, length / 2, level - 1, acc)
    acc
end

_mid(p, q) = ((p[1] + q[1]) / 2, (p[2] + q[2]) / 2)

"""Collect ``(three vertices, level)`` triangles of the gasket into ``acc``."""
function sierpinski_triangles!(points, level, acc)
    push!(acc, (points, level))
    level == 0 && return acc
    m01 = _mid(points[1], points[2])
    m02 = _mid(points[1], points[3])
    m12 = _mid(points[2], points[3])
    sierpinski_triangles!([points[1], m01, m02], level - 1, acc)
    sierpinski_triangles!([points[2], m01, m12], level - 1, acc)
    sierpinski_triangles!([points[3], m12, m02], level - 1, acc)
    acc
end
