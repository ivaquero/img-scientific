"""Unit tests for the ``imgsci new`` scaffolder (dependency-free).

These exercise the pure generation logic of :mod:`img_scientific._scaffold` --
the id parsing, the two value serializers, and the three emitted file bodies --
plus the collision guard in ``create()``. Nothing here writes into the repo, so
the tests are safe to run anywhere (``pytest`` in CI, or directly).
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from img_scientific import _scaffold


def _raises(fn, arg) -> bool:
    """Return True if ``fn(arg)`` raises ScaffoldError (kept out of loops for PERF203)."""
    try:
        fn(arg)
    except _scaffold.ScaffoldError:
        return True
    return False


def test_parse_chart_id():
    assert _scaffold.parse_chart_id("distrib/geom_pmf") == ("distrib", "geom_pmf")
    for bad in ("noSlash", "Bad/Case", "1abc/x", "topic/"):
        assert _raises(_scaffold.parse_chart_id, bad), f"expected ScaffoldError for {bad!r}"


def test_value_serializers():
    # TOML literals
    assert _scaffold._toml_value([0.1, 0.5]) == "[0.1, 0.5]"
    assert _scaffold._toml_value(True) == "true"
    assert _scaffold._toml_value("a") == '"a"'
    # Python signature defaults (immutable, so ruff B006 stays quiet)
    assert _scaffold._py_default([0.1, 0.5]) == "(0.1, 0.5)"
    assert _scaffold._py_default([3]) == "(3,)"
    assert _scaffold._py_default([]) == "()"
    assert _scaffold._py_default(True) == "True"
    assert _scaffold._py_default(5) == "5"


def test_render_spec_has_python_binding_only():
    text = _scaffold.render_spec(
        "funcs/probe", "funcs", "probe", "func_probe", "line", "Probe", {"a": 1, "b": [1, 2]}
    )
    assert 'id = "funcs/probe"' in text
    assert "[python]" in text and 'module = "img_scientific.funcs.func_probe"' in text
    assert "[params]" in text and "a = 1" in text and "b = [1, 2]" in text
    # module must NOT be a top-level key (ADR 0001)
    top = text.split("[python]")[0]
    assert "module" not in top


def test_render_python_signature_is_ruff_clean():
    text = _scaffold.render_python("funcs/probe", "probe", "Probe", {"ps": [0.1, 0.5], "n": 3})
    assert '@chart("funcs/probe")' in text
    assert "def make_probe(" in text
    assert "    ps=(0.1, 0.5)," in text  # tuple default, not a mutable list
    assert "    ps=[0.1, 0.5]," not in text
    assert "    title=\"Probe\"," in text


def test_render_julia_registers():
    text = _scaffold.render_julia("funcs/probe", "probe", "func_probe", "Probe", {"n": 3})
    assert 'register!("funcs/probe", make_probe)' in text
    assert 'p["title"]' in text


def test_create_refuses_collision_without_force():
    # "distrib/geom_pmf" already exists; create() must bail before writing.
    try:
        _scaffold.create("distrib/geom_pmf")
    except _scaffold.ScaffoldError:
        return
    raise AssertionError("expected ScaffoldError on colliding id")


def _run(fn) -> bool:
    try:
        fn()
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL {fn.__name__}: {exc}")
        return False


def _main() -> int:
    checks = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in checks:
        if _run(fn):
            print(f"ok   {fn.__name__}")
            passed += 1
    total = len(checks)
    print(f"\n{passed}/{total} scaffold checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(_main())
