"""fractals/koch_flake -- order-n Koch snowflake (mirrors img_scientific/fractals/turtle_koch_flake.py)."""

function make_koch_flake(p::AbstractDict)
    xs, ys = walk(snowflake_cmds(p["size"], p["n"]), p["start"])
    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = p["title"])
    lines!(ax, xs, ys; color = to_color(p["color"]), linewidth = p["linewidth"])
    fig
end

register!("fractals/koch_flake", make_koch_flake)
