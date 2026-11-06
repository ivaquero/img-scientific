"""metric/cov_ellipse -- covariance ellipse rings (mirrors img_scientific/metric/metric_cov_ellipse.py)."""

function make_cov_ellipse(p::AbstractDict)
    mean = _vec(p["mean"])
    cov = p["cov"]

    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "x", ylabel = "y", title = p["title"])

    for sd in p["stds"]
        xs, ys = ellipse_pts(mean, cov, Float64(sd))
        poly!(ax, xs, ys; color = to_color(p["facecolor"]), alpha = p["alpha"],
            strokecolor = to_color(p["edgecolor"]), label = "σ = $sd")
    end
    scatter!(ax, [mean[1]], [mean[2]]; color = to_color(p["edgecolor"]), marker = :cross)
    axislegend(ax; position = :ut)
    fig
end

register!("metric/cov_ellipse", make_cov_ellipse)
