"""graphs/clustering_bars -- per-node clustering coefficient bars (mirrors img_scientific/graphs/graph_clustering_bars.py)."""

function make_graph_clustering_bars(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n, k, pw = p["n"], p["k"], p["p"]
    adj = adjacency(n, watts_strogatz_edges(n, k, pw, rng))
    vals = [node_clustering(adj, u) for u in 1:n]
    mean = clustering_coefficient(adj, n)
    xs = 1:n

    fig = Figure(resolution = (700, 400))
    ax = Axis(fig[1, 1]; xlabel = "node index", ylabel = "clustering coefficient",
              ylim = (0, 1), title = p["title"])
    barplot!(ax, xs, vals; color = tab_color(p["node_color"]), alpha = 0.75)
    hlines!(ax, [mean]; linestyle = :dash, color = :orangered)
    fig
end

register!("graphs/clustering_bars", make_graph_clustering_bars)
