"""Chart registry: maps a chart id to its ``make_*`` function.

A chart module registers itself with :func:`chart` at import time. Importing a
module is the only side effect -- nothing executes a plot, because every chart
is now a function rather than top-level script code.
"""

from __future__ import annotations

from collections.abc import Callable

REGISTRY: dict[str, Callable] = {}


def chart(chart_id: str):
    """Class-free decorator binding ``chart_id`` to a make-function."""

    def decorator(func: Callable) -> Callable:
        REGISTRY[chart_id] = func
        func.chart_id = chart_id
        return func

    return decorator
