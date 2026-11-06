"""graphs/ws_lattice -- Watts-Strogatz rewiring row (mirrors img_scientific/graphs/graph_ws.py)."""

function make_graph_ws(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n, k, ps = p["n"], p["k"], p["ps"]
    col = tab_color(p["node_color"])

    fig = Figure(resolution = (400 * length(ps), 400))
    for (i, pw) in enumerate(ps)
        edges = watts_strogatz_edges(n, k, pw, rng)
        g = build_graph(n, edges)
        ax = Axis(fig[1, i]; title = @sprintf("p = %.3g", pw))
        graphplot!(ax, g; layout = :circular, labels = string.(1:n),
                   nmarkersize = p["node_size"] / 10, nodecolor = col)
    end
    Label(fig[0, :], p["title"])
    fig
end

register!("graphs/ws_lattice", make_graph_ws)
