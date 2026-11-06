"""Render pipeline: spec -> (import module) -> make-function -> figure -> PNG."""

from __future__ import annotations

import importlib
import pathlib

from . import _io, _spec
from ._registry import REGISTRY


def _ensure_registered(chart_id: str, module: str):
    if chart_id not in REGISTRY:
        importlib.import_module(module)
    if chart_id not in REGISTRY:
        msg = f"module {module!r} did not register chart {chart_id!r}"
        raise KeyError(msg)
    return REGISTRY[chart_id]


def render(
    chart_id: str,
    *,
    overrides: dict | None = None,
    out: str | pathlib.Path | None = None,
) -> pathlib.Path:
    """Render one chart by id, applying CLI ``--set`` overrides."""
    spec = _spec.load(chart_id)
    func = _ensure_registered(chart_id, spec["module"])

    params = dict(spec.get("params", {}))
    params.update(overrides or {})

    fig = func(**params)

    topic = chart_id.split("/", 1)[0]
    name = spec.get("out") or chart_id.rsplit("/", 1)[-1]
    target = pathlib.Path(out) if out else _io.images_path(topic, name)
    return _io.save(fig, target)


def gallery(topic: str | None = None) -> list[pathlib.Path]:
    """Render every chart that has a spec (optionally filtered by topic)."""
    specs = _spec.all_specs()
    ids = sorted(ids for ids in specs if topic is None or ids.startswith(f"{topic}/"))
    return [render(chart_id) for chart_id in ids]
