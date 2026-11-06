"""
Original Author: Xavier Yang
Link: https://github.com/ivaquero
"""

import matplotlib.pyplot as plt
import numpy as np

from img_scientific._registry import chart
from img_scientific._style import set_style


def _init_grid(size, rng):
    """Random +/-1 spin lattice on a ``size x size`` grid."""
    return 2 * rng.integers(2, size=(size, size)) - 1


def _wolff_step(grid, temperature, rng):
    """Flip one Wolff cluster; ``accept = 1 - exp(-2 / T)`` for same-spin links."""
    L = len(grid)
    i, j = rng.integers(0, L, size=2)

    cluster = {(i, j)}
    to_flip = {(i, j)}

    while to_flip:
        i, j = to_flip.pop()
        neighbors = [
            ((i + 1) % L, j),
            ((i - 1) % L, j),
            (i, (j + 1) % L),
            (i, (j - 1) % L),
        ]

        for ni, nj in neighbors:
            if (
                (ni, nj) not in cluster
                and grid[ni, nj] == grid[i, j]
                and rng.random() < 1 - np.exp(-2 / temperature)
            ):
                to_flip.add((ni, nj))
                cluster.add((ni, nj))

    for ci, cj in cluster:
        grid[ci, cj] = -grid[ci, cj]


def _simulate(grid_size, temperature, num_steps, rng):
    grid = _init_grid(grid_size, rng)
    history = []
    for _ in range(num_steps):
        _wolff_step(grid, temperature, rng)
        history.append(int(np.sum(grid)))
    return history


@chart("physics/ising")
def make_ising(
    *,
    grid_size=3,
    temperature=2.0,
    num_steps=1000,
    seed=1337,
    color="blue",
    title="Wolff Algorithm - 3x3 Ising Model at T=2.0",
):
    """Wolff-cluster Ising magnetisation over Monte-Carlo steps (seeded)."""
    set_style()

    rng = np.random.default_rng(seed)
    history = _simulate(grid_size, temperature, num_steps, rng)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(range(num_steps), history, color=color)
    ax.set(xlabel="Monte Carlo Steps", ylabel="Magnetization", title=title)
    return fig
