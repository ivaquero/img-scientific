"""distrib/categ_pmf -- Categorical sampling scatter (mirrors img_scientific/distrib/distrib_categ_pmf.py)."""

function make_categ_pmf(p::AbstractDict)
    prob = p["p"]
    n = p["n_trials"]
    rng = MersenneTwister(p["seed"])
    # numpy randint(0, len(p)-1) draws {0, ..., len(p)-2} (upper exclusive) --
    # reproduced so the sampled support matches the reference figure.
    y = [prob[rand(rng, 1:length(prob)-1)] for _ in 1:n]
    x = collect(0:n-1)
    μ = mean(y)
    σ = sqrt(sum((y .- μ) .^ 2) / length(y))  # population std, like np.std (ddof=0)
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; title = p["title"], xlabel = "X", ylabel = "value")
    scatter!(ax, x, y; color = :royalblue, label = @sprintf("μ=%.2f, σ=%.2f", μ, σ))
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/categ_pmf", make_categ_pmf)
