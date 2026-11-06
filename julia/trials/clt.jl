"""trials/clt -- sampling distribution of the mean of exponentials (mirrors img_scientific/trials/theo_clt.py)."""

function make_clt(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n_sim = p["n_sim"]
    ns = p["ns"]
    loc = p["loc"]

    fig = Figure(resolution = (400 * length(ns), 400))

    for (i, (n, color, alpha)) in enumerate(zip(ns, p["colors"], p["alphas"]))
        ax = Axis(fig[1, i]; title = @sprintf("%d draws from Expo(%d)", n, loc), xlabel = "X̄")
        m = n_sim * n
        e = loc .- log.(rand(rng, m))                 # loc + Exp(1)
        xbar = [sum(@view e[(k - 1) * n + 1:k * n]) / n for k in 1:n_sim]
        hist!(ax, xbar; bins = p["bins"], color = to_color(color), alpha = alpha)
        xlims!(ax, 1.25, 3.25)
    end
    fig
end

register!("trials/clt", make_clt)
