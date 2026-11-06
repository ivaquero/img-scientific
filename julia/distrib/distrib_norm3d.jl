"""distrib/norm3d -- Trivariate-normal surface (mirrors img_scientific/distrib/distrib_norm3d.py)."""

function make_norm3d(p::AbstractDict)
    gx = range(p["x_range"][1], p["x_range"][2]; length = p["n"])
    gy = range(p["y_range"][1], p["y_range"][2]; length = p["n"])
    Z = zeros(p["n"], p["n"])
    for (mean, cov) in zip(p["xs"], p["ps"])
        covmat = reduce(hcat, [Float64.(row) for row in cov])  # rows -> 2x2 matrix
        mvn = MvNormal(Float64.(collect(mean)), covmat)
        for (i, xx) in enumerate(gx)
            for (j, yy) in enumerate(gy)
                Z[i, j] += pdf(mvn, [xx, yy])
            end
        end
    end
    fig = Figure(resolution = (700, 500))
    ax = Axis3(fig[1, 1]; title = p["title"], xlabel = "x", ylabel = "y", zlabel = "z")
    surface!(ax, collect(gx), collect(gy), Z; colormap = :autumn)
    ax.azimuth = p["azim"]
    ax.elevation = p["elev"]
    fig
end

register!("distrib/norm3d", make_norm3d)
