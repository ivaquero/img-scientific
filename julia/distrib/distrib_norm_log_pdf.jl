"""distrib/norm_log_pdf -- Log-normal two-panel (mirrors img_scientific/distrib/distrib_norm_log_pdf.py)."""

function make_norm_log_pdf(p::AbstractDict)
    x = 10 .^ range(p["x_start"], p["x_stop"]; length = p["x_num"]) .+ p["offset"]
    s = p["s"]
    y = clean([pdf(LogNormal(0, s), xi) for xi in x])
    res = (p["figsize"][1] * 100, p["figsize"][2] * 100)
    fig = Figure(resolution = res)
    ax1 = Axis(fig[1, 1]; xlabel = "X", ylabel = "PDF(X)")
    xlims!(ax1, p["xlim"][1], p["xlim"][2])
    lines!(ax1, x, y; color = :royalblue)
    ax2 = Axis(fig[1, 2]; xlabel = "log(X)")
    lines!(ax2, log.(x), y; color = :royalblue)
    Label(fig[0, 1:2], p["title"], tellwidth = false; textsize = 16)
    fig
end

register!("distrib/norm_log_pdf", make_norm_log_pdf)
