"""distrib/hgeom_pmf -- Hypergeometric PMF bars (mirrors img_scientific/distrib/distrib_hgeom_pmf.py)."""

function make_hgeom_pmf(p::AbstractDict)
    X = grid_arr(p)
    ys = [[pdf(Hypergeometric(N, M, m), k) for k in X] for (N, M, m) in zip(p["Ns"], p["Ms"], p["ms"])]
    labels = ["N=$(N), M=$(M), m=$(m)" for (N, M, m) in zip(p["Ns"], p["Ms"], p["ms"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PMF(X)", title = p["title"])
    bars!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/hgeom_pmf", make_hgeom_pmf)
