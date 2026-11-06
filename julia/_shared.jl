"""
_shared.jl -- cross-topic drawing helpers for the Julia chart implementations.

Included *once* by ``charts.jl`` (before any topic directory is walked) into the
module scope that holds every ``<topic>/<chart>.jl`` file, so the per-chart files
can call these without re-declaring them (Julia has no cross-file ``import`` for
``include``d code, and redefining a ``const`` twice is an error).

This is the small amount of glue the Python package would otherwise inline in
each module -- grid construction, the colour palette, NaN-cleaning and the
``bars!`` / ``curves!`` series helpers. Topic-only helpers live in each
directory's own ``_helpers.jl``.
"""

# --- numpy-style grids -------------------------------------------------------

"""numpy-style ``arange``: half-open ``[start, stop)`` with a fixed step."""
function arange(start, stop, step)
    n = max(0, Int(ceil((stop - start) / step)))
    [start + i * step for i in 0:n-1]
end

"""numpy-style ``linspace``: ``n`` points spanning ``[a, b]``."""
grid(a, b, n) = collect(range(a, b; length = n))

# Convenience readers for the two grid conventions the specs use.
grid_lin(p) = grid(p["x_min"], p["x_max"], p["x_num"])
grid_arr(p) = arange(p["x_start"], p["x_stop"], p["x_step"])

# --- colours -----------------------------------------------------------------

"""Series colour palette for charts that leave colour to the backend."""
const PALETTE = [:gray20, :royalblue, :orangered, :seagreen, :mediumorchid, :goldenrod, :teal, :maroon]
pal(i) = PALETTE[((i - 1) % length(PALETTE)) + 1]

"""Map the spec's colour *strings* (shared with Python) to Makie colours."""
const COLOR_MAP = Dict(
    "blue" => :royalblue,
    "green" => :seagreen,
    "orange" => :darkorange,
    "red" => :orangered,
    "purple" => :mediumorchid,
    "brown" => :brown,
    "black" => :black,
)
to_color(s) = get(COLOR_MAP, string(s), pal(2))

# --- data + series helpers ---------------------------------------------------

"""Replace non-finite values with NaN so Makie draws gaps instead of exploding
(e.g. the beta PDF diverging at x=0 when a<1, cauchy/log tails)."""
clean(y) = [isfinite(v) ? float(v) : NaN for v in y]

"""Scatter/bars helper: several discrete PMF series on an integer grid."""
function bars!(ax, X, ys, alphas, labels)
    for (i, y) in enumerate(ys)
        bar!(ax, X, clean(y); color = pal(i), alpha = alphas[i], label = labels[i])
    end
    ax
end

"""Curve helper: several continuous series, optional fill-under to y=0."""
function curves!(ax, X, ys, alphas, labels; colors = nothing, fill = true, fillalpha = 0.25)
    for (i, y) in enumerate(ys)
        c = colors === nothing ? pal(i) : to_color(colors[i])
        yc = clean(y)
        if fill
            band!(ax, X, zeros(length(yc)), yc; color = c, alpha = fillalpha)
        end
        lines!(ax, X, yc; color = c, alpha = alphas[i], label = labels[i])
    end
    ax
end
