"""distrib/norm_multi_pdf -- Bivariate-normal contour grid (mirrors img_scientific/distrib/distrib_norm_multi_pdf.py)."""

function make_norm_multi_pdf(p::AbstractDict)
    g = collect(-5:0.1:4.9)  # numpy mgrid[-5:5:0.1] is half-open -> ~100 pts
    s1 = p["sigma_x1"]
    res = (p["figsize"][1] * 140, p["figsize"][2] * 100)
    fig = Figure(resolution = res)
    for (i, s2) in enumerate(p["sigma_x2s"])
        for (j, rho) in enumerate(p["rhos"])
            cov = [float(s1)^2 float(s1 * s2 * rho); float(s1 * s2 * rho) float(s2)^2]
            mvn = MvNormal(zeros(2), cov)
            Z = [pdf(mvn, [x, y]) for x in g, y in g]
            ax = Axis(fig[i, j])
            contourf!(ax, g, g, Z)
            xlims!(ax, p["xlim"][1], p["xlim"][2])
            ylims!(ax, p["ylim"][1], p["ylim"][2])
            yticks!(ax, collect(float.(p["yticks"])))
            ax.title = @sprintf("σ_x2 = %3.2f, ρ = %3.2f", s2, rho)
        end
    end
    Label(fig[0, :], p["title"], tellwidth = false; textsize = 16)
    fig
end

register!("distrib/norm_multi_pdf", make_norm_multi_pdf)
