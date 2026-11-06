"""fractals/general_dim -- multifractal τ(q), D_q and f(α) curves (mirrors img_scientific/fractals/general_dim.py)."""

# log(binomial(k, s)) as a pure-Base log-product (no SpecialFunctions): sum the
# m = min(s, k-s) leading factors of k!/(s!(k-s)!). Matches scipy.comb + log.
function _logcomb(k, s)
    m = min(s, k - s)
    m <= 0 && return 0.0
    acc = 0.0
    for i in 1:m
        acc += log(k - i + 1) - log(i)
    end
    acc
end

function make_general_dim(p::AbstractDict)
    p1, p2, k = p["p1"], p["p2"], p["k"]
    log3 = log(3.0)
    log_inv3 = log(1 / 3)

    fig = Figure(resolution = (600, 800))

    # The tau(q) curve.
    xq = grid(p["x_min"], p["x_max"], p["tau_num"])
    tau = [log(p1^q + p2^q) / log3 for q in xq]
    ax1 = Axis(fig[1, 1]; xlabel = "q", ylabel = "τ(q)")
    lines!(ax1, xq, tau)

    # The D_q curve (split at q = 1 to dodge the singularity).
    x1 = grid(p["x_min"], 0.99, p["dq_num"])
    x2 = grid(0.99, p["x_max"], p["dq_num"])
    Dq1 = [log(p1^q + p2^q) / (log3 * (1 - q)) for q in x1]
    Dq2 = [log(p2^q + p1^q) / (log3 * (1 - q)) for q in x2]
    ax2 = Axis(fig[2, 1]; xlabel = "q", ylabel = "D_q")
    lines!(ax2, x1, Dq1)
    lines!(ax2, x2, Dq2)

    # The f(alpha) singularity spectrum.
    s = collect(0:k-1)
    xa = [(si * log(p1) + (k - si) * log(p2)) / (k * log_inv3) for si in s]
    f = [-_logcomb(k, si) / (k * log_inv3) for si in s]
    ax3 = Axis(fig[3, 1]; xlabel = "α", ylabel = "f(α)")
    lines!(ax3, xa, f)

    Label(fig[0, :], p["title"])
    fig
end

register!("fractals/general_dim", make_general_dim)
