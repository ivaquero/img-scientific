"""distrib/expon_cdf -- Exponential CDF curves (mirrors img_scientific/distrib/distrib_expon_cdf.py)."""

function make_expon_cdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [_expon_cdf(X, loc) for loc in p["locs"]]
    labels = ["n=$(loc)" for loc in p["locs"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "CDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels; fill = false)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/expon_cdf", make_expon_cdf)
