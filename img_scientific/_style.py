"""Central matplotlib styling, replacing the per-script ``plt.style.use`` calls."""

from __future__ import annotations

import matplotlib.pyplot as plt

DEFAULT_STYLE = "seaborn-v0_8-dark"


def set_style(name: str = DEFAULT_STYLE) -> None:
    """Apply a named matplotlib style (default matches the legacy scripts)."""
    plt.style.use(name)
