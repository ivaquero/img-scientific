"""
_helpers.jl -- metric-topic helpers (covariance-ellipse maths, Gaussian product,
ellipse point generation). Requires LinearAlgebra (loaded by charts.jl).

Mirrors the Python helper functions that live in ``metric_utils.py``
(``multi_gaussian_product``) and ``metric_cov_ellipse.py``
(``covariance_ellipse``). The ``plot_cov_ellipse`` patch drawing is replaced by
an ellipse *polygon* (``ellipse_pts``) so it renders with Makie ``poly!``.
"""

# Accept either a real AbstractMatrix or an array-of-rows from a TOML spec.
_mat(a::AbstractMatrix) = Float64.(a)
_mat(a) = [Float64(a[i][j]) for i in 1:length(a), j in 1:length(a[1])]
_vec(a) = Float64.(collect(a))

function covariance_ellipse(cov, deviations = 1)
    F = svd(_mat(cov))
    U, s = F.U, F.S
    orientation = atan(U[2, 1], U[1, 1])
    wr = deviations * sqrt(s[1])
    hr = deviations * sqrt(s[2])
    orientation, wr, hr
end

"""Parametric outline (closed) of the ``sd``-sigma covariance ellipse about *mean*."""
function ellipse_pts(mean, cov, sd = 1)
    o, wr, hr = covariance_ellipse(cov, 1.0)
    m = _vec(mean)
    rx, ry = sd * wr, sd * hr
    ts = range(0, 2π; length = 120)
    xs = [m[1] + rx * cos(t) * cos(o) - ry * sin(t) * sin(o) for t in ts]
    ys = [m[2] + rx * cos(t) * sin(o) + ry * sin(t) * cos(o) for t in ts]
    append!(xs, [xs[1]])
    append!(ys, [ys[1]])
    xs, ys
end

"""Posterior mean/cov of the product of two Gaussians (up to a constant)."""
function multi_gaussian_product(mean1, cov1, mean2, cov2)
    m1, m2 = _vec(mean1), _vec(mean2)
    c1, c2 = _mat(cov1), _mat(cov2)
    sinv = inv(c1 + c2)
    mean = c2 * sinv * m1 + c1 * sinv * m2
    cov = c1 * sinv * c2
    mean, cov
end
