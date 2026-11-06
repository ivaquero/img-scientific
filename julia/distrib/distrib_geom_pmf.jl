"""distrib/geom_pmf -- Geometric PMF bars (mirrors img_scientific/distrib/distrib_geom_pmf.py)."""

function make_geom_pmf(p::AbstractDict)
    X = grid_arr(p)
    # Distributions Geometric is failures-based (0..); scipy geom is trials (1..).
    ys = [[k < 1 ? 0.0 : pdf(Geometric(prob), k - 1) for k in X] for prob in p["ps"]]
    labels = ["p=$(prob)" for prob in p["ps"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PMF(X)", title = p["title"])
    bars!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/geom_pmf", make_geom_pmf)
