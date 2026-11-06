"""Central matplotlib styling, replacing the per-script ``plt.style.use`` calls."""

from __future__ import annotations

import matplotlib.pyplot as plt

DEFAULT_STYLE = "seaborn-v0_8-dark"

# ``plt.style.use`` pushes a context onto matplotlib's rcParams stack every call;
# charts each call ``set_style()``, so a whole-gallery run would otherwise stack
# dozens of identical contexts. Remember the active style and skip no-op changes.
_APPLIED_STYLE: str | None = None


def set_style(name: str = DEFAULT_STYLE) -> None:
    """Apply a named matplotlib style (default matches the legacy scripts)."""
    global _APPLIED_STYLE
    if name == _APPLIED_STYLE:
        return
    plt.style.use(name)
    _APPLIED_STYLE = name
