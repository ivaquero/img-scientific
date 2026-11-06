"""distrib/norm_cdf -- Normal CDF curves (mirrors img_scientific/distrib/distrib_norm_cdf.py)."""

function make_norm_cdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[cdf(Normal(loc, sc), x) for x in X] for (loc, sc) in zip(p["locs"], p["scales"])]
    labels = ["μ=$(loc), σ=$(sc)" for (loc, sc) in zip(p["locs"], p["scales"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "CDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels; colors = p["colors"], fill = false)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/norm_cdf", make_norm_cdf)
