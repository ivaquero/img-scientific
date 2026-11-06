"""distrib/t_pdf -- Student-t PDF curves (mirrors img_scientific/distrib/distrib_t_pdf.py)."""

function make_t_pdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[pdf(TDist(df), x) for x in X] for df in p["dfs"]]
    labels = ["n=$(df)" for df in p["dfs"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels; colors = p["colors"])
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/t_pdf", make_t_pdf)
