"""physics/ising -- Wolff-cluster Ising magnetisation (mirrors img_scientific/physics/ising.py)."""

_init_grid(size, rng) = 2 .* Int.(rand(rng, Bool, size, size)) .- 1

function _wolff_step!(grid, temperature, rng)
    L = size(grid, 1)
    i, j = rand(rng, 1:L), rand(rng, 1:L)

    cluster = Set{Tuple{Int,Int}}([(i, j)])
    to_flip = Tuple{Int,Int}[(i, j)]
    p_add = 1 - exp(-2 / temperature)

    while !isempty(to_flip)
        i, j = pop!(to_flip)
        for (ni, nj) in ((mod1(i + 1, L), j), (mod1(i - 1, L), j),
                         (i, mod1(j + 1, L)), (i, mod1(j - 1, L)))
            if (ni, nj) ∉ cluster && grid[ni, nj] == grid[i, j] && rand(rng) < p_add
                push!(to_flip, (ni, nj))
                push!(cluster, (ni, nj))
            end
        end
    end

    for (ci, cj) in cluster
        grid[ci, cj] = -grid[ci, cj]
    end
end

function _simulate(grid_size, temperature, num_steps, rng)
    grid = _init_grid(grid_size, rng)
    hist = Vector{Int}(undef, num_steps)
    for s in 1:num_steps
        _wolff_step!(grid, temperature, rng)
        hist[s] = sum(grid)
    end
    hist
end

function make_ising(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    history = _simulate(p["grid_size"], p["temperature"], p["num_steps"], rng)
    fig = Figure(resolution = (800, 400))
    ax = Axis(fig[1, 1]; xlabel = "Monte Carlo Steps", ylabel = "Magnetization", title = p["title"])
    scatter!(ax, 0:p["num_steps"]-1, Float64.(history); color = to_color(p["color"]))
    fig
end

register!("physics/ising", make_ising)
