"""distrib/nbinom_pmf -- Negative-binomial PMF bars (mirrors img_scientific/distrib/distrib_nbinom_pmf.py)."""

function make_nbinom_pmf(p::AbstractDict)
    X = grid_arr(p)
    ys = [[pdf(NegativeBinomial(n, prob), k) for k in X] for (n, prob) in zip(p["ns"], p["ps"])]
    labels = ["n=$(n), p=$(prob)" for (n, prob) in zip(p["ns"], p["ps"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PMF(X)", title = p["title"])
    bars!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/nbinom_pmf", make_nbinom_pmf)
