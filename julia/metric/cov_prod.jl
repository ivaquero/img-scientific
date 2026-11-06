"""metric/cov_prod -- prior x likelihood = posterior Gaussians (mirrors img_scientific/metric/metric_cov_prod.py)."""

function make_cov_prod(p::AbstractDict)
    mean = _vec(p["mean"])
    c0 = p["cov_prior"]
    c1 = p["cov_likelihood"]
    c2 = multi_gaussian_product(mean, c0, mean, c1)[2]

    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "x", ylabel = "y", title = p["title"])

    for (cov, lab, fc, al) in ((c0, "prior", :yellow, 0.2),
                               (c1, "likelihood", :seagreen, 0.5),
                               (c2, "posterior", :navy, 0.8))
        xs, ys = ellipse_pts(mean, cov, 1.0)
        poly!(ax, xs, ys; color = fc, alpha = al, strokecolor = :black, label = lab)
    end
    axislegend(ax; position = :rb)
    fig
end

register!("metric/cov_prod", make_cov_prod)
