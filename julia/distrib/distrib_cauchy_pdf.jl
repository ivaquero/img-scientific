"""distrib/cauchy_pdf -- Cauchy PDF curves (mirrors img_scientific/distrib/distrib_cauchy_pdf.py)."""

function make_cauchy_pdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[pdf(Cauchy(loc, 1), x) for x in X] for loc in p["locs"]]
    labels = ["n=$(loc)" for loc in p["locs"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels; colors = p["colors"])
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/cauchy_pdf", make_cauchy_pdf)
