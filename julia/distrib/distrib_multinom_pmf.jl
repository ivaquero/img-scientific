"""distrib/multinom_pmf -- Multinomial coefficient scatter (mirrors img_scientific/distrib/distrib_multinom_pmf.py)."""

function make_multinom_pmf(p::AbstractDict)
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; title = p["title"], xlabel = "index", ylabel = "coefficient")
    for (idx, n_trials) in enumerate(p["n_trials_list"])
        ys = Float64[]
        for a in 1:n_trials, b in (a+1):n_trials, c in (b+1):n_trials
            if a + b + c == n_trials
                push!(ys, float(factorial(big(n_trials))) /
                    (float(factorial(big(a))) * float(factorial(big(b))) * float(factorial(big(c)))))
            end
        end
        xs = collect(0:length(ys)-1)
        scatter!(ax, xs, ys; color = pal(idx), alpha = 0.8, label = "trial = $(n_trials)")
    end
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/multinom_pmf", make_multinom_pmf)
