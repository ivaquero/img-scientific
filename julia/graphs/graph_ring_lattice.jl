"""graphs/ring_lattice -- pure ring lattice circular layout (mirrors img_scientific/graphs/graph_ring_lattice.py)."""

function make_graph_ring_lattice(p::AbstractDict)
    n, k = p["n"], p["k"]
    edges = ring_lattice_edges(n, k)
    g = build_graph(n, edges)

    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = p["title"])
    graphplot!(ax, g; layout = :circular, labels = string.(1:n),
               nmarkersize = p["node_size"] / 10, nodecolor = tab_color(p["node_color"]))
    fig
end

register!("graphs/ring_lattice", make_graph_ring_lattice)
