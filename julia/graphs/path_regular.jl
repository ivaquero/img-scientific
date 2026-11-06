"""graphs/regular -- k-regular graph network (mirrors img_scientific/graphs/path_regular.py)."""

function make_path_regular(p::AbstractDict)
    n, k = p["n"], p["k"]
    edges = regular_edges(n, k)
    g = build_graph(n, edges)

    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = p["title"])
    graphplot!(ax, g; layout = :circular, labels = string.(1:n),
               nmarkersize = p["node_size"] / 10, nodecolor = tab_color(p["node_color"]))
    fig
end

register!("graphs/regular", make_path_regular)
