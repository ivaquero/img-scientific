"""
charts.jl -- thin loader/aggregator for the Julia plotting implementations.

The chart bodies do not live here: they are split **one file per chart**, in
one-to-one correspondence with the Python modules ``img_scientific/<topic>/*.py``.
Julia has no decorators, so each chart file registers itself at the bottom with
``register!("<topic>/<id>", make_<id>)`` -- the direct analogue of Python's
``@chart("<topic>/<id>")`` decorator.

This file only wires up the environment and pulls those files in, in order:

  1. load the Makie ecosystem + numeric packages and the bridge's
     ``register!`` / ``set_saver!``
       - CairoMakie re-exports Makie, so the statistical charts use the plain
         Makie API (``bar! · lines! · band! · scatter! · contourf! · surface! ·
         poly! · Axis3``). GraphMakie (``graphplot``) is used by the ``graphs/``
         topic; it is pulled in by ``graphs/_helpers.jl``.
  2. for each topic directory that exists: include its ``_helpers.jl`` (grids,
     palette, NaN-cleaning, series helpers, and any topic-only ``using``), then
     every ``*.jl`` chart file that does not start with ``_`` (each self-registers).
  3. inject the CairoMakie ``save`` saver into the bridge.

Topic directories are auto-discovered, so adding a chart is just dropping a new
``<topic>/<name>.jl`` file -- no edit here required.

Requires CairoMakie + Distributions; ``runall.jl`` guards the include.
"""

using CairoMakie
using Distributions
using LinearAlgebra
using Printf
using Random
using Statistics
using ..ImgScientificJulia: register!, set_saver!

# --- cross-topic helpers, loaded exactly once (const-safe) -------------------

include(normpath(@__DIR__, "_shared.jl"))

# --- per-topic helpers, then every chart file in that topic ------------------

const _TOPICS = [
    "distrib",   # 30 distribution pdf/pmf/cdf + sampling charts
    "funcs",     # elementary math functions (sigmoid ...)
    "physics",   # simulation charts (Ising ...)
    "trials",    # sampling / CLT / LLT demonstration charts
    "metric",    # covariance / information metrics
    "fractals",  # fern, dimension, Koch / Sierpinski (turtle -> line segments)
    "graphs",    # network layouts (GraphMakie) and path / metric charts
]

for topic in _TOPICS
    dir = normpath(@__DIR__, topic)
    isdir(dir) || continue

    helpers = joinpath(dir, "_helpers.jl")
    isfile(helpers) && include(helpers)

    for file in sort(readdir(dir))
        (endswith(file, ".jl") && !startswith(file, "_")) || continue
        include(joinpath(dir, file))
    end
end

# --- the only place that knows how to write a Makie figure to disk -----------

set_saver!((fig, path) -> save(path, fig))
