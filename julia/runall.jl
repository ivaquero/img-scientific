"""
runall.jl -- render every shared-spec chart that has a Julia implementation.

Flow:
  1. load the TOML-only bridge (always works -- stdlib ``TOML``).
  2. try to load the CairoMakie/Distributions implementations. If those
     packages are missing, keep going and just report what *would* render.
  3. walk the full spec set (the shared source of truth) and render the ids we
     have implemented; warn-and-skip the ones we do not (yet).

Run it from the ``julia/`` directory:

    julia runall.jl
"""

include("common.jl")
using .ImgScientificJulia

plotting = try
    include("charts.jl")
    true
catch err
    @warn "plotting packages not available -- skipping render (install with `] instantiate` in julia/Project.toml)" exception = (err, catch_backtrace())
    false
end

ids = all_ids()
println("discovered $(length(ids)) shared specs; $(length(registered())) have a Julia impl")

rendered = String[]
for id in ids
    if id in registered()
        path = render(id)
        push!(rendered, path)
        println("  rendered $id -> $path")
    else
        @info "no Julia impl yet, skipping" id = id
    end
end

println("done: $(length(rendered)) figure(s) written under images/julia/")
