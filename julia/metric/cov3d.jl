"""metric/cov3d -- 3-sigma covariance ellipsoid + samples (mirrors img_scientific/metric/metric_cov3d.py)."""

function make_cov3d(p::AbstractDict)
    mean = _vec(p["mean"])
    cov = _mat(p["cov"])
    sd = Float64(p["std"])
    N = p["n"]
    m = p["n_samples"]

    ev = eigen(Symmetric(cov))
    radii = sd .* sqrt.(max.(ev.values, 0.0))
    evec = ev.vectors

    u = range(0, 2π; length = N)
    v = range(0, π; length = N)
    X = Matrix{Float64}(undef, N, N)
    Y = similar(X)
    Z = similar(X)
    for (i, uu) in enumerate(u)
        for (j, vv) in enumerate(v)
            w = evec * [radii[1] * cos(uu) * sin(vv), radii[2] * sin(uu) * sin(vv), radii[3] * cos(vv)]
            X[i, j] = w[1] + mean[1]
            Y[i, j] = w[2] + mean[2]
            Z[i, j] = w[3] + mean[3]
        end
    end

    fig = Figure(resolution = (500, 500))
    ax = Axis3(fig[1, 1]; xlabel = "X", ylabel = "Y", zlabel = "Z", title = p["title"])
    surface!(ax, X, Y, Z; alpha = p["alpha"], color = :lightblue)

    rng = MersenneTwister(p["seed"])
    L = cholesky(Symmetric(cov)).L
    g = L * randn(rng, 3, m)
    sx = [g[1, k] + mean[1] for k in 1:m]
    sy = [g[2, k] + mean[2] for k in 1:m]
    sz = [g[3, k] + mean[3] for k in 1:m]
    scatter!(ax, sx, sy, sz; color = :orangered, marker = :circle, markersize = 3)
    fig
end

register!("metric/cov3d", make_cov3d)
