"""graphs/ws_sampled -- Monte-Carlo sampled characteristic path length L(p) (mirrors img_scientific/graphs/graph_ws_sampled.py)."""

function make_graph_ws_sampled(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n, k, iters, trials, ps = p["n"], p["k"], p["iters"], p["trials"], p["ps"]

    ls = Float64[]
    for pw in ps
        vals = Float64[]
        for _ in 1:iters
            adj = adjacency(n, watts_strogatz_edges(n, k, pw, rng))
            push!(vals, estimate_path_length(adj, n, rng, trials))
        end
        push!(ls, sum(vals) / length(vals))
    end

    fig = Figure(resolution = (700, 400))
    ax = Axis(fig[1, 1]; xlabel = "rewiring probability p", ylabel = "mean path length",
              xscale = log10, title = p["title"])
    lines!(ax, ps, ls; color = :seagreen, label = @sprintf("sampled (trials=%d, iters=%d)", trials, iters))
    scatter!(ax, ps, ls; color = :seagreen)
    axislegend(ax; position = :rt)
    fig
end

register!("graphs/ws_sampled", make_graph_ws_sampled)
