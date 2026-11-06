"""distrib/f_pdf -- F-distribution PDF curves (mirrors img_scientific/distrib/distrib_f_pdf.py)."""

function make_f_pdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[pdf(FDist(dfn, dfd), x) for x in X] for (dfn, dfd) in zip(p["locs"], p["loc2s"])]
    labels = ["n1=$(dfn), n2=$(dfd)" for (dfn, dfd) in zip(p["locs"], p["loc2s"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PMF(X)", title = p["title"])  # "PMF" quirk mirrored from Python
    curves!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/f_pdf", make_f_pdf)
