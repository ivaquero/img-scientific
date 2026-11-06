"""trials/conv_unif -- histogram of the sum of two uniforms (mirrors img_scientific/trials/conv_unif.py)."""

function make_conv_unif(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    n = p["n_trials"]
    t = rand(rng, n) + rand(rng, n)

    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "x + y", ylabel = "Frequency", title = p["title"])
    hist!(ax, vec(t); bins = p["bins"], color = to_color(p["color"]))
    fig
end

register!("trials/conv_unif", make_conv_unif)
