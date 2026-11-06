"""distrib/unif_cdf -- Uniform CDF curves (mirrors img_scientific/distrib/distrib_unif_cdf.py)."""

function make_unif_cdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[cdf(Uniform(loc, loc + sc), x) for x in X] for (loc, sc) in zip(p["locs"], p["scales"])]
    labels = ["loc=$(loc), scale=$(sc)" for (loc, sc) in zip(p["locs"], p["scales"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "CDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels; fill = false)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/unif_cdf", make_unif_cdf)
