"""graphs/connectivity -- P(connected) vs p phase transition (mirrors img_scientific/graphs/graph_connectivity.py)."""

function make_graph_connectivity(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n, iters, ps = p["n"], p["iters"], p["ps"]
    probs = [prob_connected(n, pw, iters, rng) for pw in ps]
    threshold = log(n) / n

    fig = Figure(resolution = (700, 400))
    ax = Axis(fig[1, 1]; xlabel = "edge probability p", ylabel = "fraction connected",
              ylim = (-0.05, 1.05), title = p["title"])
    lines!(ax, ps, probs; color = :seagreen, label = @sprintf("empirical (n=%d, iters=%d)", n, iters))
    scatter!(ax, ps, probs; color = :seagreen)
    vlines!(ax, [threshold]; linestyle = :dash, color = :orangered,
            label = @sprintf("p = log(n)/n = %.3f", threshold))
    axislegend(ax; position = :rb)
    fig
end

register!("graphs/connectivity", make_graph_connectivity)
