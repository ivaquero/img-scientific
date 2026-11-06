"""funcs/logit_odds -- logit and odds vs probability (mirrors img_scientific/funcs/func_logit_odds.py)."""

function make_func_logit_odds(p::AbstractDict)
    pmin, pmax, pn = p["p_min"], p["p_max"], p["p_num"]
    xs = grid(pmin, pmax, pn)
    odds = [v / (1 - v) for v in xs]
    logits = [log(o) for o in odds]

    fig = Figure(resolution = (700, 400))

    ax_odds = Axis(fig[1, 1]; xlabel = "probability", ylabel = "odds",
                   xlim = (pmin, pmax), ylim = (0, odds[end]),
                   title = p["title"])
    lines!(ax_odds, xs, odds; color = to_color(p["odds_color"]))

    ax_right = Axis(fig[1, 1]; ylabel = "logit", yaxisposition = :right,
                    limits = (pmin, pmax, logits[begin], logits[end]))
    lines!(ax_right, xs, logits; color = to_color(p["logit_color"]))
    ax_right.xgridvisible = false
    ax_right.ygridvisible = false
    fig
end

register!("funcs/logit_odds", make_func_logit_odds)
