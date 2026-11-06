"""fractals/sierpinski_square -- recursive quarter-squares (mirrors img_scientific/fractals/turtle_sierpinski_square.py)."""

function make_sierpinski_square(p::AbstractDict)
    outer, inner = to_color(p["outer_color"]), to_color(p["inner_color"])
    acc = Tuple{Float64, Float64, Float64, Int}[]
    sierpinski_squares!(p["start"][1], p["start"][2], p["length"], p["level"], acc)

    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = p["title"])
    for (x, y, side, lvl) in acc
        xs = [x, x + side, x + side, x, x]
        ys = [y, y, y + side, y + side, y]
        lines!(ax, xs, ys; color = lvl == 0 ? outer : inner)
    end
    fig
end

register!("fractals/sierpinski_square", make_sierpinski_square)
