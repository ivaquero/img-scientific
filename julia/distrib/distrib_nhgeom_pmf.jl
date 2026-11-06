"""distrib/nhgeom_pmf -- Negative-hypergeometric PMF bars (mirrors img_scientific/distrib/distrib_nhgeom_pmf.py)."""

"""Negative-hypergeometric PMF (no Distributions.jl type); mirrors scipy.

scipy nhypergeom(M, n, N) pmf(x) = C(M,x) C(n, N-x) / C(M+n, N), with the Python
call ``nhypergeom(N, M, r)`` mapping M->N, n->M, N->r.
"""
function nhypergeom_pmf(x, M, n, N)
    lo = max(0, N - n)
    hi = min(M, N)
    (x < lo || x > hi) && return 0.0
    float(binomial(M, x) * binomial(n, N - x)) / float(binomial(M + n, N))
end

function make_nhgeom_pmf(p::AbstractDict)
    X = grid_arr(p)
    ys = [[nhypergeom_pmf(k, N, M, r) for k in X] for (N, M, r) in zip(p["Ns"], p["Ms"], p["rs"])]
    labels = ["N=$(N), M=$(M), r=$(r)" for (N, M, r) in zip(p["Ns"], p["Ms"], p["rs"])]
    fig = Figure(resolution = (600, 400))
    ax = Axis(fig[1, 1]; xlabel = "X", ylabel = "PMF(X)", title = p["title"])
    bars!(ax, X, ys, p["alphas"], labels)
    axislegend(ax; position = :rt)
    fig
end

register!("distrib/nhgeom_pmf", make_nhgeom_pmf)
