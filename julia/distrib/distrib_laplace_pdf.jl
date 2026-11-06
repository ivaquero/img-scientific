"""distrib/laplace_pdf -- Laplace PDF curves + Gaussian reference (mirrors img_scientific/distrib/distrib_laplace_pdf.py)."""

function make_laplace_pdf(p::AbstractDict)
    X = grid_lin(p)
    ys = [[pdf(Laplace(loc, sc), x) for x in X] for (loc, sc) in zip(p["locs"], p["scales"])]
    labels = ["μ=$(loc), σ=$(sc)" for (loc, sc) in zip(p["locs"], p["scales"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])
    curves!(ax, X, ys, p["alphas"], labels; colors = p["colors"])
    lines!(ax, X, [pdf(Normal(0, 1), x) for x in X]; color = :orangered, alpha = 0.8, label = "Gaussian")
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/laplace_pdf", make_laplace_pdf)
