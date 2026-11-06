"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import special

from .._registry import chart
from .._style import set_style


@chart("distrib/dirichlet_pdf")
def make_dirichlet_pdf(
    *,
    alpha_lists=((1, 1, 1), (1, 1, 3), (2, 2, 6), (2, 2, 2)),
    alphas=(0.3, 0.4, 0.5, 0.6),
    n_exp=1200,
    seed=42,
    title="Dirichlet Distribution",
):
    """Line chart of sampled Dirichlet PDF values for several alpha vectors."""
    set_style()

    # One generator for the whole chart. The old code re-seeded
    # ``np.random.default_rng(seed)`` inside ``sampling`` on every call, so all
    # ``n_exp`` draws were identical and each alpha vector collapsed to a flat
    # horizontal density line. Seeding once lets the draws actually vary.
    rng = np.random.default_rng(seed)

    def sampling(s=1):
        x = rng.randint(1, 100, size=(3, 1))
        return [s * (xi / sum(x)) for xi in x]

    def beta_function(α):
        a1, a2, a3 = α
        return (
            special.gamma(a1)
            * special.gamma(a2)
            * special.gamma(a3)
            / special.gamma(sum(α))
        )

    def dirichlet(x, α, n_trails):
        """
        :param x: list of [x[1,...,K], x[1,...,K], ...], shape is (n_trial, K)
        """
        c = 1 / beta_function(α)
        y = []
        for xn in x:
            prods = [xi ** (ai - 1) for xi, ai in zip(xn, α, strict=True)]
            y.append(np.prod(prods, initial=c))

        x = np.arange(n_trails)
        return x, y, np.mean(y), np.std(y)

    # Draw the simplex samples once; scoring the same points under each alpha
    # makes the four density curves directly comparable. ``dirichlet`` does not
    # mutate its input, so reusing ``samples`` across the loop is safe.
    samples = [sampling() for _ in range(n_exp)]

    fig, ax = plt.subplots()
    for ls, alpha in zip(alpha_lists, alphas, strict=True):
        α = np.array(ls)
        x, y, _, _ = dirichlet(samples, α, n_trails=n_exp)
        ax.plot(x, y, label=f"$α=({ls[0]}, {ls[1]}, {ls[2]})$", alpha=alpha)

    ax.set(title=title)
    ax.legend()
    return fig
