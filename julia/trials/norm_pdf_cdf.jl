"""trials/norm_pdf_cdf -- normal PDF (shaded) and CDF panels (mirrors img_scientific/trials/stats_norm_pdf_cdf.py)."""

function make_norm_pdf_cdf(p::AbstractDict)
    loc = p["loc"]
    x_min = p["x_min"]
    x_max = p["x_max"]
    f = Normal(loc, p["scale"])
    x = grid(x_min, x_max, p["x_num"])

    ix = grid(x_min, loc, 50)
    iy = [pdf(f, xi) for xi in ix]
    polyx = [x_min; ix; loc; x_min]
    polyy = [0.0; iy; 0.0; 0.0]

    fig = Figure(resolution = (800, 400))

    ax1 = Axis(fig[1, 1]; xlabel = "x", ylabel = "PDF(x)")
    lines!(ax1, x, [pdf(f, xi) for xi in x])
    poly!(ax1, polyx, polyy; color = :lightgray, strokecolor = :gray)
    text!(ax1, 0.2 * (x_min + loc), 0.25 * pdf(f, loc); text = "CDF(x)", align = :center)

    ax2 = Axis(fig[1, 2]; xlabel = "x", ylabel = "CDF(x)")
    lines!(ax2, x, [cdf(f, xi) for xi in x])
    scatter!(ax2, [loc], [cdf(f, loc)]; color = :blue, marker = :circle)
    vlines!(ax2, loc; linestyle = :dash)

    Label(fig[0, :], p["title"])
    fig
end

register!("trials/norm_pdf_cdf", make_norm_pdf_cdf)
