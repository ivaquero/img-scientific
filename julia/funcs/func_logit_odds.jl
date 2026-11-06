"""funcs/logit_odds -- logit and odds vs probability (mirrors img_scientific/funcs/func_logit_odds.py)."""

function make_func_logit_odds(p::AbstractDict)
    pmin, pmax, pn = p["p_min"], p["p_max"], p["p_num"]
    xs = grid(pmin, pmax, pn)
    odds = [v / (1 - v) for v in xs]
    logits = [log(o) for o in odds]

    fig = Figure(resolution = (700, 400))

    ax_left = Axis(fig[1, 1]; xlabel = "probability p", ylabel = "logit(p)",
                   xlim = (pmin, pmax), title = p["title"])
    lines!(ax_left, xs, logits; color = to_color(p["logit_color"]), label = "logit(p)")

    ax_right = Axis(fig[1, 1]; ylabel = "odds(p) = p / (1 - p)",
                    yscale = log10, yaxisposition = :right)
    lines!(ax_right, xs, odds; color = to_color(p["odds_color"]), linestyle = :dash,
           label = "odds(p)")
    ax_right.xgridvisible = false
    ax_right.ygridvisible = false

    axislegend(ax_left; position = :lt)
    fig
end

register!("funcs/logit_odds", make_func_logit_odds)
