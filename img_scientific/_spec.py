"""Language-neutral chart specs (``img_scientific/specs/**/*.toml``).

A *spec* is the single source of truth for what a chart is and the default
parameters used to draw it. Both the Python renderer and (later) the Julia
Makie renderer read the same spec, which is what prevents the kind of drift
we already saw between the old Python and Julia ``geom_pmf`` files.

Spec keys
---------
id      : str  -- "topic/name", e.g. "distrib/geom_pmf" (also the spec path)
title   : str
kind    : str  -- pmf | pdf | cdf | hist | network | ...
module  : str  -- dotted Python module that registers this chart
out     : str  -- output PNG stem (kept equal to the legacy image filename)
params  : dict -- keyword defaults passed to the chart function
"""

from __future__ import annotations

import pathlib

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # Python 3.10 fallback
    import tomli as tomllib  # type: ignore[no-redef]

# <repo>/img_scientific/_spec.py -> parent == img_scientific (specs live inside the package)
SPEC_ROOT = pathlib.Path(__file__).resolve().parent / "specs"


def spec_path(chart_id: str) -> pathlib.Path:
    topic, _, name = chart_id.partition("/")
    return SPEC_ROOT / topic / f"{name}.toml"


def load(chart_id: str) -> dict:
    """Read and parse one chart spec by id."""
    with spec_path(chart_id).open("rb") as fh:
        return tomllib.load(fh)


def all_specs() -> dict[str, dict]:
    """Return ``{chart_id: spec}`` for every spec on disk (no imports needed)."""
    specs: dict[str, dict] = {}
    for path in sorted(SPEC_ROOT.rglob("*.toml")):
        with path.open("rb") as fh:
            spec = tomllib.load(fh)
        chart_id = spec.get("id") or f"{path.parent.name}/{path.stem}"
        specs[chart_id] = spec
    return specs


def coerce(value: str):
    """Best-effort typing for a CLI ``--set key=value`` scalar.

    Supports ``int``, ``float``, ``bool``, comma-separated lists, else ``str``.
    """
    text = value.strip()
    lowered = text.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if "," in text:
        return [coerce(part) for part in text.split(",")]
    for cast in (int, float):
        try:
            return cast(text)
        except ValueError:
            continue
    return text


def parse_set(items) -> dict:
    """Parse ``["k=v", "arr=1,2,3"]`` into a typed dict for chart overrides."""
    overrides: dict = {}
    for item in items or []:
        key, _, raw = item.partition("=")
        if not _:
            msg = f"--set expects key=value, got {item!r}"
            raise ValueError(msg)
        overrides[key.strip()] = coerce(raw)
    return overrides
