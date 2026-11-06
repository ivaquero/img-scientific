"""graphs/cluster_size -- component-size histogram via DFS reachability (mirrors img_scientific/graphs/graph_cluster_size.py)."""

function make_graph_cluster_size(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n, pw = p["n"], p["p"]
    edges = er_np_edges(n, pw, rng)
    adj = adjacency(n, edges)
    sizes = cluster_sizes(adj, n)

    fig = Figure(resolution = (700, 400))
    ax = Axis(fig[1, 1]; xlabel = "reachable-set size (nodes)", ylabel = "count",
              xlim = (0, n + 1), title = p["title"])
    histogram!(ax, sizes; bins = 1:n+1, color = :steelblue)
    fig
end

register!("graphs/cluster_size", make_graph_cluster_size)
