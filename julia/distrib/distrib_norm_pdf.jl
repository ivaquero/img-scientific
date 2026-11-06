"""distrib/norm_pdf -- Normal PDF curves (mirrors img_scientific/distrib/distrib_norm_pdf.py)."""

function make_norm_pdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[pdf(Normal(loc, sc), x) for x in X] for (loc, sc) in zip(p["locs"], p["scales"])]
    labels = ["μ=$(loc), σ=$(sc)" for (loc, sc) in zip(p["locs"], p["scales"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels; colors = p["colors"])
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/norm_pdf", make_norm_pdf)
