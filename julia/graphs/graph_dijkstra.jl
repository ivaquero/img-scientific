"""graphs/dijkstra -- level-sweeping shortest-path distances on a ring lattice (mirrors img_scientific/graphs/graph_dijkstra.py)."""

function make_graph_dijkstra(p::AbstractDict)
    n, k = p["n"], p["k"]
    edges = ring_lattice_edges(n, k)
    adj = adjacency(n, edges)
    dists = bfs_dists(adj, n, p["source"] + 1)
    g = build_graph(n, edges)

    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = p["title"], aspect = DataAspect())
    graphplot!(ax, g; layout = :circular, labels = string.(1:n),
               nmarkersize = p["node_size"] / 10,
               nodecolor = dists, nodecolormap = :bamboo)
    fig
end

register!("graphs/dijkstra", make_graph_dijkstra)
