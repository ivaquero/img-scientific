"""``imgsci new`` -- scaffold one chart across the whole L1 contract.

Adding a chart by hand means keeping *three* things in sync on the exact same
``id``: a Python module (``@chart`` + a ``make_*``), a spec ``.toml`` (the single
source of truth), and a Julia file (``register!`` + a ``make_*``). This helper
generates a self-consistent, contract-passing skeleton for all three from one
command so the boilerplate (and the copy-paste drift it invites) is eliminated.
The plotting bodies are left as ``TODO`` stubs -- the author fills in the *how*.

Everything here is stdlib-only so it runs (and can generate charts) without
matplotlib / numpy / CairoMakie installed.
"""

from __future__ import annotations

import pathlib
import re

from . import _spec

REPO = pathlib.Path(__file__).resolve().parent.parent
PKG = REPO / "img_scientific"
SPEC_ROOT = PKG / "specs"
JULIA = REPO / "julia"

_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")


class ScaffoldError(ValueError):
    """Raised for bad arguments or collisions (so the CLI can print + exit 2)."""


def parse_chart_id(chart_id: str) -> tuple[str, str]:
    """Split ``topic/name`` and validate both parts are identifier-safe."""
    topic, sep, name = chart_id.partition("/")
    if not sep:
        msg = f"chart id must look like '<topic>/<id>', got {chart_id!r}"
        raise ScaffoldError(msg)
    for part in (topic, name):
        if not _NAME_RE.match(part):
            msg = f"'{part}' is not a lowercase identifier ([a-z][a-z0-9_]*)"
            raise ScaffoldError(msg)
    return topic, name


def _default_out(topic: str, name: str) -> str:
    return f"{topic}_{name}"


def _default_title(name: str) -> str:
    return name.replace("_", " ").replace("-", " ").strip().capitalize()


def _toml_value(value) -> str:
    """Serialize a Python value to a TOML scalar/array literal."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        text = repr(value)
        return text
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_toml_value(v) for v in value) + "]"
    # string / anything else -> quoted
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _py_default(value) -> str:
    """Serialize a default for a generated Python signature (repo convention).

    Lists become immutable tuple literals so ruff's B006 (mutable default) never
    fires, matching how the existing charts write e.g. ``ps=(0.1, 0.5, 0.8)``.
    """
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (list, tuple)):
        if not value:
            return "()"
        inner = ", ".join(_py_default(v) for v in value)
        return f"({inner},)" if len(value) == 1 else f"({inner})"
    return _toml_value(value)


def render_spec(chart_id: str, topic: str, name: str, out: str, kind: str,
                title: str, params: dict) -> str:
    module = f"img_scientific.{topic}.{out}"
    lines = [
        f'id = "{chart_id}"',
        f'title = {_toml_value(title)}',
        f"kind = {_toml_value(kind)}",
        f"out = {_toml_value(out)}",
        "",
        "[python]",
        f"module = {_toml_value(module)}",
        "",
        "[params]",
    ]
    for key, value in params.items():
        lines.append(f"{key} = {_toml_value(value)}")
    return "\n".join(lines) + "\n"


def render_python(chart_id: str, fn: str, title: str, params: dict) -> str:
    kw = [f"    {key}={_py_default(val)}," for key, val in params.items()]
    kw.append(f"    title={_py_default(title)},")
    body = "\n".join(kw)
    return (
        f'"""{chart_id} -- {title}."""\n'
        "\n"
        "from __future__ import annotations\n"
        "\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "from img_scientific._registry import chart\n"
        "from img_scientific._style import set_style\n"
        "\n"
        "\n"
        f'@chart("{chart_id}")\n'
        f"def make_{fn}(\n"
        "    *,\n"
        f"{body}\n"
        "):\n"
        f'    """TODO({chart_id}): implement and return the matplotlib Figure."""\n'
        "    set_style()\n"
        "\n"
        "    fig, ax = plt.subplots()\n"
        "    ax.set(title=title)\n"
        "    return fig\n"
    )


def render_julia(chart_id: str, fn: str, out: str, title: str, params: dict) -> str:
    reads = ""
    if params:
        reads = (
            "    # Parameters arrive from the shared spec; read them by name.\n"
            + "".join(f'    # {key} = p["{key}"]\n' for key in params)
        )
    return (
        f'"""{chart_id} -- {title} (mirrors img_scientific/{chart_id.split("/")[0]}/{out}.py)."""\n'
        "\n"
        f"function make_{fn}(p::AbstractDict)\n"
        f"    # TODO({chart_id}): draw here using the shared-spec parameters.\n"
        f"{reads}"
        "    fig = Figure(resolution = (600, 400))\n"
        '    ax = Axis(fig[1, 1]; title = p["title"])\n'
        "    fig\n"
        "end\n"
        "\n"
        f'register!("{chart_id}", make_{fn})\n'
    )


def _ensure_pkg_init(topic_dir: pathlib.Path) -> None:
    init = topic_dir / "__init__.py"
    if not init.exists():
        init.write_text(f'"""img_scientific.{topic_dir.name} charts."""\n', encoding="utf-8")


def _ensure_topic_in_loader(topic: str) -> bool:
    """Add ``topic`` to charts.jl's ``_TOPICS`` if it is missing. Returns changed."""
    loader = JULIA / "charts.jl"
    if not loader.exists():
        return False
    text = loader.read_text(encoding="utf-8")
    if f'"{topic}"' in text:
        return False
    marker = "const _TOPICS = ["
    if marker not in text:
        return False
    text = text.replace(marker, f'{marker}\n    "{topic}",', 1)
    loader.write_text(text, encoding="utf-8")
    return True


def create(chart_id: str, *, kind: str = "chart", title: str | None = None,
           out: str | None = None, params: dict | None = None,
           force: bool = False) -> list[pathlib.Path]:
    """Write the spec + Python + Julia skeleton for ``chart_id``. Returns paths."""
    topic, name = parse_chart_id(chart_id)
    out = out or _default_out(topic, name)
    if not _NAME_RE.match(out):
        msg = f"--out '{out}' is not a lowercase identifier"
        raise ScaffoldError(msg)
    title = title if title is not None else _default_title(name)
    params = dict(params or {})
    fn = name

    spec_path = SPEC_ROOT / topic / f"{name}.toml"
    py_path = PKG / topic / f"{out}.py"
    jl_path = JULIA / topic / f"{out}.jl"

    targets = {spec_path, py_path, jl_path}
    if not force:
        clash = sorted(str(p.relative_to(REPO)) for p in targets if p.exists())
        if clash:
            msg = "already exists (pass --force to overwrite): " + ", ".join(clash)
            raise ScaffoldError(msg)
        module = f"img_scientific.{topic}.{out}"
        if module in {
            s.get("python", {}).get("module") for s in _spec.all_specs().values()
        }:
            msg = f"another spec already uses [python].module '{module}'; pass --out to differ"
            raise ScaffoldError(msg)

    spec_path.parent.mkdir(parents=True, exist_ok=True)
    py_path.parent.mkdir(parents=True, exist_ok=True)
    jl_path.parent.mkdir(parents=True, exist_ok=True)
    _ensure_pkg_init(py_path.parent)

    spec_path.write_text(render_spec(chart_id, topic, name, out, kind, title, params), encoding="utf-8")
    py_path.write_text(render_python(chart_id, fn, title, params), encoding="utf-8")
    jl_path.write_text(render_julia(chart_id, fn, out, title, params), encoding="utf-8")

    _ensure_topic_in_loader(topic)
    return [spec_path, py_path, jl_path]
