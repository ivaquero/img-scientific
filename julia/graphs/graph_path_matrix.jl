"""graphs/path_matrix -- all-pairs shortest-path distance heatmap (mirrors img_scientific/graphs/graph_path_matrix.py)."""

function make_graph_path_matrix(p::AbstractDict)
    n, k = p["n"], p["k"]
    edges = ring_lattice_edges(n, k)
    adj = adjacency(n, edges)
    mat = Matrix{Int}(undef, n, n)
    for u in 1:n
        d = bfs_dists(adj, n, u)
        for v in 1:n
            mat[u, v] = d[v]
        end
    end
    L = characteristic_path_length(adj, n)

    fig = Figure(resolution = (600, 500))
    ax = Axis(fig[1, 1];
              xlabel = "target v", ylabel = "source u",
              xticks = (1:n, string.(1:n)), yticks = (1:n, string.(1:n)),
              title = @sprintf("%s\nring lattice G(%d,%d) · mean L = %.2f", p["title"], n, k, L))
    hm = heatmap!(ax, mat; colormap = Symbol(p["cmap"]))
    Colorbar(fig[1, 2], hm; label = "hops")
    fig
end

register!("graphs/path_matrix", make_graph_path_matrix)
