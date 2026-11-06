"""distrib/gamma_cdf -- Gamma CDF curves (mirrors img_scientific/distrib/distrib_gamma_cdf.py)."""

function make_gamma_cdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[cdf(Gamma(a, lam), x) for x in X] for (a, lam) in zip(p["a_params"], p["scale_params"])]
    labels = [@sprintf("a = %2.1f, λ = %2.1f", a, lam) for (a, lam) in zip(p["a_params"], p["scale_params"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])  # "PDF" quirk mirrored from Python
    curves!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/gamma_cdf", make_gamma_cdf)
