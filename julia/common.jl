"""
ImgScientificJulia -- the Julia side of the L1 "spec contract".

This module reuses the *same* language-neutral chart specs that the Python
package uses (``../img_scientific/specs/**/*.toml``). A spec is the single
source of truth for a chart's identity, default parameters, output filename
and title. Nothing here re-declares those values; they are read straight from
the shared TOML at runtime. That is what stops Python and Julia from drifting
apart (the old ``distrib_bin_pmf.jl`` had actually turned into a Poisson plot
and ``distrib_geom_pmf.jl`` was a random-sampling histogram -- both ignored the
spec and the analytic definition).

Design split (mirrors the Python ``_spec/_io/_registry/_render`` layering):

  * this file  -- pure bridge: TOML reading, path layout, id->impl registry.
                  Needs only stdlib ``TOML`` so ``all_specs`` / ``out_path`` /
                  ``registered`` work even before CairoMakie is installed.
  * charts.jl  -- the plotting implementations (CairoMakie + Distributions).
                  Registers ``id -> function`` entries into ``CHARTS``.
  * runall.jl  -- drives everything: iterate specs, render registered ids,
                  skip + warn the ones with no Julia impl yet.

A chart implementation is ``function(params::AbstractDict) -> Figure``; it
reads keyword defaults *from the spec dict*, so the parameter contract is
identical across languages.
"""
module ImgScientificJulia

using TOML

export SPEC_ROOT, IMAGES_ROOT, all_specs, all_ids, params, spec, spec_file
export title, kind, out_name, out_path, topic
export registered, register!, unimplemented, render, gallery, set_saver!

# --- shared-spec location (single source of truth, shared with Python) -------
const HERE = dirname(@__FILE__)
const SPEC_ROOT = normpath(HERE, "..", "img_scientific", "specs")

# Output layout: Julia images land in their own subtree so bilingual re-renders
# never clobber the Python references. This one constant is the only place that
# decides it (same idea as Python's ``_io.IMAGES_ROOT``).
const IMAGES_ROOT = normpath(HERE, "..", "images", "julia")

"""
    all_specs() -> Dict{String, Dict}

Parse every ``specs/**/*.toml`` into ``{id => spec}`` (id is the spec's own
``id`` field, or ``topic/filename`` as a fallback). Stdlib-only, no plotting
packages required.
"""
function all_specs()
    specs = Dict{String, Dict}()
    for (root, _, files) in walkdir(SPEC_ROOT)
        for f in files
            endswith(f, ".toml") || continue
            path = joinpath(root, f)
            spec = TOML.parsefile(path)
            id = get(spec, "id", string(basename(root), "/", splitext(f)[1]))
            specs[id] = spec
        end
    end
    specs
end

"""
    spec_file(id) -> String

Map a chart id ("topic/name") to its shared spec path ("specs/topic/name.toml"),
mirroring Python's ``_spec.spec_path``.
"""
function spec_file(id)::String
    parts = split(id, "/")
    if length(parts) == 2
        normpath(SPEC_ROOT, parts[1], parts[2] * ".toml")
    else
        normpath(SPEC_ROOT, id * ".toml")
    end
end

"""
    spec(id) -> Dict
"""
spec(id) = TOML.parsefile(spec_file(id))

"""
    params(id; overrides=Dict()) -> Dict

The chart's default parameters from the shared spec, with optional overrides
applied on top (mirrors Python ``{**spec['params'], **overrides}``).
"""
function params(id; overrides::AbstractDict = Dict())
    p = copy(get(spec(id), "params", Dict{String, Any}()))
    for (k, v) in overrides
        p[string(k)] = v
    end
    p
end

topic(id) = split(id, "/")[1]
out_name(id) = get(spec(id), "out", split(id, "/")[end])
title(id) = get(spec(id), "title", id)
kind(id) = get(spec(id), "kind", "chart")

"""
    out_path(id) -> String

``<IMAGES_ROOT>/<topic>/<out>.png`` -- the Julia-rendered sibling of the Python
image under ``images/<topic>/``.
"""
function out_path(id)::String
    mkpath(joinpath(IMAGES_ROOT, topic(id)))
    joinpath(IMAGES_ROOT, topic(id), out_name(id) * ".png")
end

# --- id -> implementation registry (Julia has no decorators) -----------------
const CHARTS = Dict{String, Function}()

"""
    register!(id, f)

Bind a chart id to a plotting function ``f(params::AbstractDict) -> Figure``.
Called from ``charts.jl``.
"""
function register!(id, f)
    CHARTS[id] = f
    return f
end

registered() = sort(collect(keys(CHARTS)))

"""
    all_ids() -> Vector{String}

Every chart id discovered in the shared specs (sorted), regardless of whether a
Julia implementation exists yet.
"""
all_ids() = sort(collect(keys(all_specs())))

"""
    unimplemented() -> Vector{String}

Spec ids that have no Julia implementation registered.
"""
function unimplemented()
    have = Set(registered())
    filter(id -> !(id in have), all_ids())
end

"""
    render(id; overrides=Dict())

Look up the Julia implementation for ``id`` and draw it from the shared-spec
parameters, saving to ``out_path(id)``. Raises a clear error if this id has no
Julia impl (i.e. ``charts.jl`` was not loaded or the chart is not ported yet).
"""
function render(id; overrides::AbstractDict = Dict())
    haskey(CHARTS, id) ||
        error("no Julia implementation for '$id' (registered: $(registered())) -- load charts.jl or port this chart")
    p = params(id; overrides)
    # The spec's top-level ``title`` is part of the shared contract; inject it as
    # the default so implementations render the same heading as Python. But honour
    # an explicit ``--set title=`` override: params() has already merged overrides
    # into ``p``, so only fill title when it is absent (matches Python, where
    # title is a make_* kwarg default that overrides win against).
    if !haskey(p, "title")
        p["title"] = get(spec(id), "title", id)
    end
    fig = CHARTS[id](p)
    path = out_path(id)
    CairoMakie_save(fig, path)
    return path
end

"""
    gallery(; ids=registered())

Render every registered id and return the list of written paths.
"""
function gallery(; ids = registered())
    [render(id) for id in ids]
end

# Saving is only possible once CairoMakie is loaded (charts.jl injects it).
const _saver = Ref{Union{Function, Nothing}}(nothing)
function set_saver!(f)
    _saver[] = f
    nothing
end
function CairoMakie_save(fig, path)
    isnothing(_saver[]) && error("plotting backend not loaded -- include(\"charts.jl\") first")
    _saver[](fig, path)
end

end # module
