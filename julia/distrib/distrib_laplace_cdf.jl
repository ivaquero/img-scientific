"""distrib/laplace_cdf -- Laplace CDF curves + Gaussian reference (mirrors img_scientific/distrib/distrib_laplace_cdf.py)."""

function make_laplace_cdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[cdf(Laplace(loc, sc), x) for x in X] for (loc, sc) in zip(p["locs"], p["scales"])]
    labels = ["μ=$(loc), σ=$(sc)" for (loc, sc) in zip(p["locs"], p["scales"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "CDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels; colors = p["colors"], fill = false)
    lines!(ax, X, [cdf(Normal(0, 1), x) for x in X]; color = :orangered, alpha = 0.8, label = "Gaussian")
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/laplace_cdf", make_laplace_cdf)
