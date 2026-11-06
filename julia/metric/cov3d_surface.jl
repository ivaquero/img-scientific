"""metric/cov3d_surface -- 100x bivariate-normal PDF surface (mirrors img_scientific/metric/metric_cov3d_surface.py)."""

function make_cov3d_surface(p::AbstractDict)
    mean = _vec(p["mean"])
    cov = _mat(p["cov"])
    g = p["grid"]

    o, wr, hr = covariance_ellipse(cov, 3.0)
    wx = abs(wr * cos(o) + hr * sin(o)) * 1.2
    wy = abs(hr * cos(o) - wr * sin(o)) * 1.2
    w = max(wx, wy)
    minx, maxx = mean[1] - w, mean[1] + w
    miny, maxy = mean[2] - w, mean[2] + w

    xs = collect(range(minx, maxx; length = g))
    ys = collect(range(miny, maxy; length = g))
    mv = MvNormal(mean, cov)
    Z = [100 * pdf(mv, [x, y]) for x in xs, y in ys]

    fig = Figure(resolution = (500, 500))
    ax = Axis3(fig[1, 1]; xlabel = "X", ylabel = "Y", zlabel = "PDF", title = p["title"])
    surface!(ax, xs, ys, Z; colormap = :autumn)
    fig
end

register!("metric/cov3d_surface", make_cov3d_surface)
