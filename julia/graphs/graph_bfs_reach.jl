"""graphs/bfs_reach -- BFS reachable component highlighted on G(n, p) (mirrors img_scientific/graphs/graph_bfs_reach.py)."""

function make_graph_bfs_reach(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n, pw = p["n"], p["p"]
    edges = er_np_edges(n, pw, rng)
    adj = adjacency(n, edges)
    reach = bfs_dists(adj, n, p["start"] + 1) .>= 0
    g = build_graph(n, edges)
    cols = [r ? :orangered : :gray40 for r in reach]

    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = @sprintf("%s — |reach| = %d", p["title"], sum(reach)))
    graphplot!(ax, g; layout = :circular, labels = string.(1:n),
               nmarkersize = p["node_size"] / 10, nodecolor = cols)
    fig
end

register!("graphs/bfs_reach", make_graph_bfs_reach)
