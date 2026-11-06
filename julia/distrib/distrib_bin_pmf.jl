"""distrib/bin_pmf -- Binomial PMF bars (mirrors img_scientific/distrib/distrib_bin_pmf.py)."""

function make_bin_pmf(p::AbstractDict)
    X = grid_arr(p)
    ys = [[pdf(Binomial(n, prob), k) for k in X] for (n, prob) in zip(p["ns"], p["ps"])]
    labels = ["N=$(n), p=$(prob)" for (n, prob) in zip(p["ns"], p["ps"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "x", ylabel = "PMF(X)", title = p["title"])
    bars!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/bin_pmf", make_bin_pmf)
