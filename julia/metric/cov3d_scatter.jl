"""metric/cov3d_scatter -- 2D sample lifted to z=0 + marginal PDF contour (mirrors img_scientific/metric/metric_cov3d_scatter.py).

matplotlib projects marginal PDFs onto the x/z and y/z planes via ``contour(zdir=)``;
Makie has no equivalent plane-projected contour, so the marginals are drawn as a
single 2-D filled contour in an adjacent axis. The 3-D scatter is kept faithful.
"""

function make_cov3d_scatter(p::AbstractDict)
    mean = _vec(p["mean"])
    cov = _mat(p["cov"])
    count = p["count"]
    g = p["grid"]

    o, wr, hr = covariance_ellipse(cov, 3.0)
    wx = abs(wr * cos(o) + hr * sin(o)) * 1.2
    wy = abs(hr * cos(o) - wr * sin(o)) * 1.2
    w = max(wx, wy)
    minx, maxx = mean[1] - w, mean[1] + w
    miny, maxy = mean[2] - w, mean[2] + w

    rng = MersenneTwister(p["seed"])
    L = cholesky(Symmetric(cov)).L
    gm = L * randn(rng, 2, count)
    px = [gm[1, k] + mean[1] for k in 1:count]
    py = [gm[2, k] + mean[2] for k in 1:count]

    xs = collect(range(minx, maxx; length = g))
    ys = collect(range(miny, maxy; length = g))
    mv = MvNormal(mean, cov)
    Z = [100 * pdf(mv, [x, y]) for x in xs, y in ys]

    fig = Figure(resolution = (800, 400))
    ax = Axis3(fig[1, 1]; xlabel = "X", ylabel = "Y", zlabel = "Z", title = p["title"])
    scatter!(ax, px, py, zeros(count); color = :orangered, marker = :circle, markersize = 2)

    ax2 = Axis(fig[1, 2]; xlabel = "X", ylabel = "Y", title = "marginal PDF")
    contourf!(ax2, xs, ys, Z; colormap = :grays)
    fig
end

register!("metric/cov3d_scatter", make_cov3d_scatter)
