"""metric/sem -- sample with ±SD and ±SEM bands (mirrors img_scientific/metric/metric_sem.py)."""

function make_sem(p::AbstractDict)
    size = p["size"]
    shift = p["mean_shift"]

    rng = MersenneTwister(p["seed"])
    x = randn(rng, size) .+ shift

    m = mean(x)
    sd = std(x)               # corrected=true (ddof=1), matches np.std(..., ddof=1)
    sem = sd / sqrt(size)     # stats.sem

    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "observation", ylabel = "value", title = p["title"])

    scatter!(ax, 1:size, x; marker = :circle, markersize = 3, color = :royalblue)
    hlines!(ax, m; color = :orange)
    hlines!(ax, m + sd; linestyle = :dash)
    hlines!(ax, m - sd; linestyle = :dash)
    hlines!(ax, m + sem; linestyle = :dash, color = :red)
    hlines!(ax, m - sem; linestyle = :dash, color = :red)

    arrows!(ax, [10], [m], [0], [sd]; color = :black)
    arrows!(ax, [10], [m], [0], [-sd]; color = :black)
    arrows!(ax, [35], [m - 5 * sem], [0], [4 * sem]; color = :black)
    arrows!(ax, [35], [m + 5 * sem], [0], [-4 * sem]; color = :black)
    text!(ax, 10, 5.5; text = " ± SD")
    text!(ax, 35, 5.2; text = " ± SEM")
    text!(ax, 75, 5.5; text = "mean")
    fig
end

register!("metric/sem", make_sem)
