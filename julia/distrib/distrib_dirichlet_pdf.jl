"""distrib/dirichlet_pdf -- Dirichlet sampled-PDF lines (mirrors img_scientific/distrib/distrib_dirichlet_pdf.py).

Single seeded generator draws the simplex samples once, then scores the same
points under each alpha vector -- mirroring the Python Dirichlet re-seed fix so
the density curves actually vary instead of collapsing to flat lines.
"""

function make_dirichlet_pdf(p::AbstractDict)
    rng = MersenneTwister(p["seed"])
    # Normalised uniform triples ~ Dirichlet(1,1,1); score each under alpha.
    samples = let s = 1
        map(1:p["n_exp"]) do _
            v = rand(rng, 1:99, 3)
            s .* (v ./ sum(v))
        end
    end
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; title = p["title"], xlabel = "draw", ylabel = "PDF")
    for (i, ls) in enumerate(p["alpha_lists"])
        d = Dirichlet(Float64.(collect(ls)))
        y = [pdf(d, s) for s in samples]
        lines!(ax, collect(0:length(y)-1), clean(y); color = pal(i), alpha = p["alphas"][i],
            label = "α=($(join(ls, ", ")))")
    end
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/dirichlet_pdf", make_dirichlet_pdf)
