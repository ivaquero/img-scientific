"""graphs/random_nm -- Erdos-Renyi G(n, m) network (mirrors img_scientific/graphs/graph_er.py)."""

function make_graph_er(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n = p["n"]
    edges = er_nm_edges(n, p["m"], rng)
    g = build_graph(n, edges)

    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = p["title"])
    graphplot!(ax, g; layout = :circular, labels = string.(1:n),
               nmarkersize = p["node_size"] / 10, nodecolor = tab_color(p["node_color"]))
    fig
end

register!("graphs/random_nm", make_graph_er)
