"""trials/lln -- running mean of Bernoulli(p) trials converging to p (mirrors img_scientific/trials/theo_lln.py)."""

function make_lln(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n = p["n_sim"]
    pp = p["p"]

    x = Int.(rand(rng, n) .< pp)
    xbar = cumsum(x) ./ (1:n)

    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; title = p["title"], xlabel = "n: number of trials", ylabel = "X̄ₙ")

    lines!(ax, 1:n, xbar; label = "X̄")
    hlines!(ax, pp, 0, n; linestyle = :dot, alpha = 0.5, label = @sprintf("p=%s", string(pp)))

    xlims!(ax, 0, n)
    yticks!(ax, Float64.(p["yticks"]))
    axislegend(ax; position = :rt)
    fig
end

register!("trials/lln", make_lln)
