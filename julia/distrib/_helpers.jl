"""
_helpers.jl -- shared drawing helpers for the Julia chart implementations.

Included *first* by ``charts.jl`` into the module scope that also holds every
``distrib/distrib_*.jl`` file, so the per-chart files can call these without
re-declaring them (Julia has no cross-file ``import`` for ``include``d code).
This is the small amount of glue the Python package would otherwise inline in
each module -- grid construction, the colour palette, NaN-cleaning and the
``bars!`` / ``curves!`` series helpers.
"""

# --- numpy-style grids -------------------------------------------------------

"""numpy-style ``arange``: half-open ``[start, stop)`` with a fixed step."""
function arange(start, stop, step)
    n = max(0, Int(ceil((stop - start) / step)))
    [start + i * step for i in 0:n-1]
end

"""numpy-style ``linspace``: ``x_num`` points spanning ``[x_min, x_max]``."""
grid_lin(p) = collect(range(p["x_min"], p["x_max"]; length = p["x_num"]))
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

# --- exponential shift helpers (shared by the pdf and cdf charts) ------------

# Exponential is shifted by ``loc`` (scipy expon(loc=)), scale fixed at 1.
_expon_pdf(X, loc) = [pdf(Exponential(1), x - loc) for x in X]
_expon_cdf(X, loc) = [cdf(Exponential(1), x - loc) for x in X]
