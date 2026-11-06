"""distrib/expon_pdf -- Exponential PDF curves (mirrors img_scientific/distrib/distrib_expon_pdf.py)."""

function make_expon_pdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [_expon_pdf(X, loc) for loc in p["locs"]]
    labels = ["n=$(loc)" for loc in p["locs"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/expon_pdf", make_expon_pdf)
