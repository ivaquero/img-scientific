"""distrib/poisson_pmf -- Poisson PMF bars (mirrors img_scientific/distrib/distrib_poisson_pmf.py)."""

function make_poisson_pmf(p::AbstractDict)
    X = grid_arr(p)
    ys = [[pdf(Poisson(λ), k) for k in X] for λ in p["lambdas"]]
    labels = ["λ=$(λ)" for λ in p["lambdas"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PMF(X)", title = p["title"])
    bars!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/poisson_pmf", make_poisson_pmf)
