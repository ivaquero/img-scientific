"""distrib/chi2_pdf -- Chi-square PDF curves (mirrors img_scientific/distrib/distrib_chi2_pdf.py)."""

function make_chi2_pdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[pdf(Chisq(loc), x) for x in X] for loc in p["locs"]]
    labels = ["n=$(loc)" for loc in p["locs"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/chi2_pdf", make_chi2_pdf)
