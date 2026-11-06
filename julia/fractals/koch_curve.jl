"""fractals/koch_curve -- order-n Koch curve (mirrors img_scientific/fractals/turtle_koch_curve.py)."""

function make_koch_curve(p::AbstractDict)
    xs, ys = walk(koch_cmds(p["size"], p["n"]), p["start"])
    fig = Figure(resolution = (640, 320))
    ax = Axis(fig[1, 1]; xlabel = "x", ylabel = "y", title = p["title"])
    lines!(ax, xs, ys; color = to_color(p["color"]), linewidth = p["linewidth"])
    fig
end

register!("fractals/koch_curve", make_koch_curve)
