"""distrib/bern_pmf -- Bernoulli PMF bars (mirrors img_scientific/distrib/distrib_bern_pmf.py)."""

function make_bern_pmf(p::AbstractDict)
    X = grid_arr(p)
    ys = [[pdf(Bernoulli(prob), k) for k in X] for prob in p["ps"]]
    labels = ["p=$(prob)" for prob in p["ps"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PMF(X)", title = p["title"])
    bars!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/bern_pmf", make_bern_pmf)
