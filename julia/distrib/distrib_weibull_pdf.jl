"""distrib/weibull_pdf -- Weibull PDF curves (mirrors img_scientific/distrib/distrib_weibull_pdf.py)."""

function make_weibull_pdf(p::AbstractDict)
    X = arange(p["x_start"], p["x_stop"], p["x_step"])
    ys = [[pdf(Weibull(k, 1), x) for x in X] for k in p["ks"]]
    labels = [@sprintf("k = %0.1f", k) for k in p["ks"]]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)", title = p["title"])
    curves!(ax, X, ys, ones(length(p["ks"])), labels; fill = false)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/weibull_pdf", make_weibull_pdf)
