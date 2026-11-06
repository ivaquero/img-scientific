"""trials/norm_3sigma -- normal PDF with 1σ/2σ/3σ bands shaded (mirrors img_scientific/trials/stats_norm_3sigma.py)."""

function make_norm_3sigma(p::AbstractDict)
    loc = p["loc"]
    scale = p["scale"]
    ns = p["n_sigma"]
    X = grid(p["x_min"], p["x_max"], p["x_num"])
    f = Normal(loc, scale)

    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; title = p["title"], xlabel = "X", ylabel = "PDF(X)")
    lines!(ax, X, [pdf(f, x) for x in X]; color = :red, alpha = p["alphas"][end])

    for i in 1:ns
        lo = loc - scale * i
        hi = loc + scale * i
        y_fall = cdf(f, hi) - cdf(f, lo)
        xd = [x for x in X if lo <= x <= hi]
        yd = [pdf(f, x) for x in xd]
        band!(ax, xd, zeros(length(yd)), yd; color = to_color(p["colors"][i]),
            alpha = p["alphas"][i], label = @sprintf("i = %d, %% = %.3f", i, y_fall))
    end

    xlims!(ax, p["x_min"], p["x_max"])
    ylims!(ax, p["y_min"], p["y_max"])
    axislegend(ax; position = :rt)
    fig
end

register!("trials/norm_3sigma", make_norm_3sigma)
