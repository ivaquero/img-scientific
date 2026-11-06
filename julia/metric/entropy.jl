"""metric/entropy -- empirical vs. true vs. uniform PMF entropy (mirrors img_scientific/metric/metric_entropy.py)."""

_entropy(v) = -sum(y * log(y) for y in v if y > 0; init = 0.0)

function make_entropy(p::AbstractDict)
    n = p["n"]
    pp = p["p"]
    xmax = p["x_max"]
    size = p["rvs_size"]

    rng = MersenneTwister(p["seed"])
    x = collect(0:xmax-1)

    # Binomial(n, p) sampled as a sum of n Bernoulli(p) draws (pure Random).
    draws = [sum(rand(rng) < pp for _ in 1:n) for _ in 1:size]
    emp = [count(==(i), draws) / size for i in x]

    q = Binomial(n, pp)
    qp = [pdf(q, xi) for xi in x]
    rp = fill(1 / xmax, xmax)

    fig = Figure(resolution = (400 * length(x) ÷ 3, 400))
    for (i, (dist, lab)) in enumerate(((emp, "true_distribution"), (qp, "q"), (rp, "r")))
        d = Float64.(dist)
        ax = Axis(fig[1, i]; title = @sprintf("%s  H=%.2f", lab, _entropy(d)), ylabel = "PMF")
        bar!(ax, x, d; color = :royalblue)
        xticks!(ax, x)
    end
    fig
end

register!("metric/entropy", make_entropy)
