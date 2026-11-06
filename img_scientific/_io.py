"""Output path + saving helpers (single source of truth for the image layout).

``IMAGES_ROOT`` is intentionally the *only* place that decides where PNGs land.
To switch to a bilingual layout later (``images/python/...`` vs
``images/julia/...``), change this one constant -- no chart code changes.
"""

from __future__ import annotations

import pathlib

# <repo>/img_scientific/_io.py -> parent.parent == <repo>
IMAGES_ROOT = pathlib.Path(__file__).resolve().parent.parent / "images"

DEFAULT_DPI = 150


def images_path(topic: str, name: str, root: str | pathlib.Path | None = None) -> pathlib.Path:
    """Return ``<IMAGES_ROOT>/<topic>/<name>.png`` without touching the disk."""
    base = pathlib.Path(root) if root is not None else IMAGES_ROOT
    return base / topic / f"{name}.png"


def save(fig, path: str | pathlib.Path, dpi: int = DEFAULT_DPI) -> pathlib.Path:
    """Persist a matplotlib ``Figure`` to *path*, creating parent dirs."""
    target = pathlib.Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(target, dpi=dpi)
    return target
