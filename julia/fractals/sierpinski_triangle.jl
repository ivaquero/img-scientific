"""fractals/sierpinski_triangle -- recursive filled gasket triangles (mirrors img_scientific/fractals/turtle_sierpinski_triangle.py)."""

function make_sierpinski_triangle(p::AbstractDict)
    cm = p["colormap"]
    ec = to_color(p["edgecolor"])
    acc = Tuple{Vector, Int}[]
    sierpinski_triangles!(p["points"], p["level"], acc)

    fig = Figure(resolution = (600, 600))
    ax = Axis(fig[1, 1]; title = p["title"])
    for (tri, lvl) in acc
        xs = [t[1] for t in tri]
        ys = [t[2] for t in tri]
        poly!(ax, xs, ys; color = to_color(cm[lvl + 1]), strokecolor = ec, linewidth = 0.3)
    end
    fig
end

register!("fractals/sierpinski_triangle", make_sierpinski_triangle)
