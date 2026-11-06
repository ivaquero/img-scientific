"""graphs/complete_digraph -- complete directed graph (mirrors img_scientific/graphs/graph_random_d.py)."""

function make_graph_random_d(p::AbstractDict)
    n = p["n"]
    arcs = [(i, j) for i in 1:n for j in 1:n if i != j]
    g = build_digraph(n, arcs)

    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = p["title"])
    graphplot!(ax, g; layout = :circular, labels = string.(1:n), arrows = :straight,
               nmarkersize = p["node_size"] / 10, nodecolor = tab_color(p["node_color"]))
    fig
end

register!("graphs/complete_digraph", make_graph_random_d)
