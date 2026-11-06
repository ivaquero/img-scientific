"""funcs/sigmoid -- logistic (sigmoid) curve (mirrors img_scientific/funcs/func_sigmoid.py)."""

_sig(z) = 1 / (1 + exp(-z))

function make_sigmoid(p::AbstractDict)
    z = grid(p["z_min"], p["z_max"], p["z_num"])
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "z", ylabel = "logistic(z)", title = p["title"])
    lines!(ax, z, [_sig(v) for v in z]; color = to_color(p["color"]))
    fig
end

register!("funcs/sigmoid", make_sigmoid)
