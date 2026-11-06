"""trials/prod_gaussian -- product of two Gaussian pdfs (mirrors img_scientific/trials/prod_gaussian.py)."""

_gauss_prod(g1, g2) = ((g1[2] * g2[1] + g2[2] * g1[1]) / (g1[2] + g2[2]),
    (g1[2] * g2[2]) / (g1[2] + g2[2]))

function make_prod_gaussian(p::AbstractDict)
    xs = grid(p["x_min"], p["x_max"], p["x_num"])
    g1 = (p["mean_1"], p["var_1"])
    g2 = (p["mean_2"], p["var_2"])
    gp = _gauss_prod(g1, g2)

    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; title = p["title"])

    for (g, ls) in zip((g1, g2, gp), (:solid, :solid, :dash))
        m, v = g
        ys = [pdf(Normal(m, sqrt(v)), x) for x in xs]
        lines!(ax, xs, ys; linestyle = ls, label = @sprintf("N(%.2f, %.2f)", m, v))
    end
    axislegend(ax; position = :lt)
    fig
end

register!("trials/prod_gaussian", make_prod_gaussian)
