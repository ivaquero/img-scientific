"""
charts.jl -- thin loader/aggregator for the Julia plotting implementations.

The chart bodies no longer live here: they are split **one file per chart**, in
one-to-one correspondence with the Python modules ``img_scientific/distrib/
distrib_*.py``. Julia has no decorators, so each ``distrib/distrib_*.jl`` file
registers itself at the bottom with ``register!("distrib/<id>", make_<id>)`` --
the direct analogue of Python's ``@chart("distrib/<id>")`` decorator.

This file only wires up the environment and pulls those files in, in order:

  1. load the Makie ecosystem + statistics packages and the bridge's
     ``register!`` / ``set_saver!``
       - CairoMakie re-exports Makie, so the statistical charts use the plain
         Makie API (``bar! · lines! · band! · scatter! · contourf! · surface! ·
         Axis3``). GraphMakie (``graphplot``) is reserved for the future
         ``graphs/`` topic and is declared in ``Project.toml``.
  2. include the shared helpers (``distrib/_helpers.jl``) -- grids, palette,
     NaN-cleaning and the ``bars!`` / ``curves!`` series helpers.
  3. include every ``distrib/distrib_*.jl`` chart (each self-registers).
  4. inject the CairoMakie ``save`` saver into the bridge.

Requires CairoMakie + Distributions; ``runall.jl`` guards the include.
"""

using CairoMakie
using Distributions
using Printf
using Random
using Statistics
using ..ImgScientificJulia: register!, set_saver!

# --- shared helpers, then every chart file (each registers itself) -----------

const _DISTRIB_DIR = normpath(@__DIR__, "distrib")

include(joinpath(_DISTRIB_DIR, "_helpers.jl"))

for file in sort(readdir(_DISTRIB_DIR))
    (endswith(file, ".jl") && !startswith(file, "_")) || continue
    include(joinpath(_DISTRIB_DIR, file))
end

# --- the only place that knows how to write a Makie figure to disk -----------

set_saver!((fig, path) -> save(path, fig))
