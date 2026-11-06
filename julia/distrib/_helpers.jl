"""
_helpers.jl -- distrib-topic-only helpers.

The general drawing glue (grids, palette, ``to_color``, ``clean``, ``bars!``,
``curves!``) now lives in the cross-topic ``../_shared.jl`` (loaded once by
``charts.jl``). This file keeps only what is specific to the distribution
charts: the location-shifted exponential pdf/cdf (Distributions' ``Exponential``
has no ``loc`` parameter, unlike scipy's ``expon(loc=)``, so we shift by hand).
"""

# Exponential is shifted by ``loc`` (scipy expon(loc=)), scale fixed at 1.
_expon_pdf(X, loc) = [pdf(Exponential(1), x - loc) for x in X]
_expon_cdf(X, loc) = [cdf(Exponential(1), x - loc) for x in X]
