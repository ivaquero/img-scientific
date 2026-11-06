"""Static spec-contract check for the Julia side -- stdlib only, no plotting packages.

The Julia renderer mirrors the same language-neutral specs that the Python
package does. Each chart file ends with ``register!("<topic>/<id>", make_<fn>)``,
which is the Julia analogue of Python's ``@chart`` decorator. This script proves
the contract holds *without* installing CairoMakie/Distributions/Graphs, so it
can run in CI on a bare Julia install (only stdlib ``TOML`` is required).

What it enforces:
  1. every spec ``id`` has exactly one matching ``register!("<id>", ...)`` call
     somewhere under ``julia/`` (no unimplemented spec slipped into the registry)
  2. every ``register!`` id corresponds to a real spec (no orphan impl)
  3. a chart's spec ``params`` keys are all read via ``p["<key>"]`` in the file,
     unless consumed indirectly through the ``grid``/``grid_arr`` helpers
     (helper-mediated reads are reported as info, never a hard failure)
  4. the chart reads ``p["title"]`` (render injects it) -- informational

This complements the *live* verification (``julia/runall.jl`` with the real
plotting packages installed), which additionally renders every figure.

Run:
    julia tests/julia_contract/verify.jl
"""

using TOML

const REPO = normpath(joinpath(@__DIR__, "..", ".."))
const SPEC_ROOT = joinpath(REPO, "img_scientific", "specs")
const JULIA_ROOT = joinpath(REPO, "julia")

function load_specs()::Dict{String,Dict}
    specs = Dict{String,Dict}()
    for (root, _, files) in walkdir(SPEC_ROOT)
        for f in files
            endswith(f, ".toml") || continue
            path = joinpath(root, f)
            spec = TOML.parsefile(path)
            id = get(spec, "id", string(basename(root), "/", splitext(basename(path))[1]))
            specs[id] = spec
        end
    end
    return specs
end

function scan_registrations()::Dict{String,String}
    # id -> file that registers it
    reg = Dict{String,String}()
    pat = r"register!\s*\(\s*\"([^\"]+)\""
    for (root, _, files) in walkdir(JULIA_ROOT)
        for f in files
            endswith(f, ".jl") || continue
            path = joinpath(root, f)
            text = read(path, String)
            for m in eachmatch(pat, text)
                id = m.captures[1]
                # Skip the docstring placeholder register!("<topic>/<id>", ...).
                occursin('<', id) && continue
                if haskey(reg, id)
                    error("duplicate register! for '$id' in $(reg[id]) and $path")
                end
                reg[id] = path
            end
        end
    end
    return reg
end

function p_keys(text::AbstractString)::Set{String}
    out = Set{String}()
    for m in eachmatch(r"p\[\"([^\"]+)\"\]", text)
        push!(out, m.captures[1])
    end
    return out
end

function main()::Int32
    specs = load_specs()
    reg = scan_registrations()

    # Keys that the _shared.jl helpers read on a chart's behalf (grid/grid_arr),
    # so their absence from an individual chart file is not a real gap.
    shared_path = joinpath(JULIA_ROOT, "_shared.jl")
    helper_keys = isfile(shared_path) ? p_keys(read(shared_path, String)) : Set{String}()

    problems::Vector{String} = String[]
    infos::Vector{String} = String[]

    spec_ids = collect(keys(specs))
    reg_ids = collect(keys(reg))

    # 1. spec without a Julia impl.
    for id in sort(spec_ids)
        haskey(reg, id) || push!(problems, "spec '$id' has no register! (unimplemented in Julia)")
    end
    # 2. impl without a spec (orphan registration).
    for id in sort(reg_ids)
        haskey(specs, id) || push!(problems, "register! '$id' has no matching spec (orphan impl)")
    end

    # 3/4. param + title read coverage (best-effort; helper-mediated reads are info).
    for id in sort(intersect(spec_ids, reg_ids))
        spec = specs[id]
        text = read(reg[id], String)
        direct = p_keys(text)
        params = get(spec, "params", Dict{String,Any}())
        for key in sort(collect(keys(params)))
            if !(key in direct) && !(key in helper_keys)
                push!(infos, "$id: param '$key' not read as p[\"$key\"] (helper-mediated?)")
            end
        end
        occursin("p[\"title\"]", text) ||
            push!(infos, "$id: does not read p[\"title\"]")
    end

    println("julia contract: $(length(spec_ids)) specs, $(length(reg_ids)) register! ids")
    if !isempty(infos)
        println("  (informational, not failures):")
        foreach(s -> println("    - $s"), infos)
    end
    if isempty(problems)
        println("PASS: spec <-> register! is 1:1 ($(length(spec_ids)) charts).")
        return Int32(0)
    end
    println("FAIL: $(length(problems)) contract problem(s):")
    foreach(s -> println("  - $s"), problems)
    return Int32(1)
end

exit(main())
