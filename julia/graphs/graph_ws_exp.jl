"""graphs/ws_experiment -- normalized C(p) and L(p) small-world curves (mirrors img_scientific/graphs/graph_ws_exp.py)."""

function make_graph_ws_exp(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n, k, iters, ps = p["n"], p["k"], p["iters"], p["ps"]

    ls, cs = Float64[], Float64[]
    for pw in ps
        sl, sc = 0.0, 0.0
        for _ in 1:iters
            adj = adjacency(n, watts_strogatz_edges(n, k, pw, rng))
            sl += characteristic_path_length(adj, n)
            sc += clustering_coefficient(adj, n)
        end
        push!(ls, sl / iters)
        push!(cs, sc / iters)
    end
    L = ls ./ ls[1]
    C = cs ./ cs[1]

    fig = Figure(resolution = (700, 400))
    ax = Axis(fig[1, 1]; xlabel = "Rewiring probability (p)", xscale = log10,
              xlim = (0.00009, 1.1), ylim = (-0.01, 1.01), title = p["title"])
    lines!(ax, ps, C; color = :seagreen)
    scatter!(ax, ps, C; color = :seagreen, marker = :rect, label = "C(p) / C(0)")
    lines!(ax, ps, L; color = :orangered)
    scatter!(ax, ps, L; color = :orangered, marker = :circle, label = "L(p) / L(0)")
    axislegend(ax; position = :rb)
    fig
end

register!("graphs/ws_experiment", make_graph_ws_exp)
