"""distrib/unif_pdf -- Uniform PDF curves (mirrors img_scientific/distrib/distrib_unif_pdf.py)."""

function make_unif_pdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[pdf(Uniform(loc, loc + sc), x) for x in X] for (loc, sc) in zip(p["locs"], p["scales"])]
    labels = ["loc=$(loc), scale=$(sc)" for (loc, sc) in zip(p["locs"], p["scales"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :lt)
    fig
end

register!("distrib/unif_pdf", make_unif_pdf)
