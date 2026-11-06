"""distrib/beta_cdf -- Beta CDF curves (mirrors img_scientific/distrib/distrib_beta_cdf.py)."""

function make_beta_cdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[cdf(Beta(a, b), x) for x in X] for (a, b) in zip(p["a_params"], p["b_params"])]
    labels = [@sprintf("a = %2.1f, b = %2.1f", a, b) for (a, b) in zip(p["a_params"], p["b_params"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "CDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/beta_cdf", make_beta_cdf)
