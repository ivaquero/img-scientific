"""``imgsci`` command line interface.

Sub-commands
------------
list                 List every chart that has a spec (no plotting deps needed).
render <id>          Render one chart, optionally overriding parameters.
gallery [--topic]    Re-render all charts (or one topic) into images/.
"""

from __future__ import annotations

import argparse
import sys

from . import _render, _spec


def _cmd_list(_: argparse.Namespace) -> int:
    specs = _spec.all_specs()
    if not specs:
        print("no specs found under img_scientific/specs/")
        return 0
    for chart_id in sorted(specs):
        spec = specs[chart_id]
        print(f"{chart_id:<24} {spec.get('kind', ''):<8} {spec.get('title', '')}")
    return 0


def _cmd_render(args: argparse.Namespace) -> int:
    overrides = _spec.parse_set(args.set)
    path = _render.render(args.chart_id, overrides=overrides, out=args.out)
    print(f"wrote {path}")
    return 0


def _cmd_gallery(args: argparse.Namespace) -> int:
    paths = _render.gallery(topic=args.topic)
    for path in paths:
        print(f"wrote {path}")
    print(f"rendered {len(paths)} chart(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="imgsci", description="Scientific plotting toolkit CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list all available charts")
    p_list.set_defaults(func=_cmd_list)

    p_render = sub.add_parser("render", help="render one chart by id")
    p_render.add_argument("chart_id", help="e.g. distrib/geom_pmf")
    p_render.add_argument(
        "--set",
        action="append",
        metavar="KEY=VALUE",
        help="override a parameter (repeatable); lists use commas, e.g. --set ps=0.1,0.5",
    )
    p_render.add_argument("--out", help="explicit output PNG path")
    p_render.set_defaults(func=_cmd_render)

    p_gallery = sub.add_parser("gallery", help="re-render charts into images/")
    p_gallery.add_argument("--topic", help="restrict to one topic, e.g. distrib")
    p_gallery.set_defaults(func=_cmd_gallery)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
