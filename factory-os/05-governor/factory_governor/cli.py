from __future__ import annotations

import argparse
import json
from pathlib import Path

from .governor import govern
from .report import render_markdown, write_json, write_markdown


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Scan a Codex environment and build a non-destructive governance plan.")
    p.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    p.add_argument("--user-home", type=Path, default=Path.home())
    p.add_argument("--repo", type=Path)
    p.add_argument("--json-out", type=Path)
    p.add_argument("--md-out", type=Path)
    p.add_argument("--format", choices=("json", "markdown"), default="markdown")
    return p


def main() -> int:
    args = build_parser().parse_args()
    report = govern(args.codex_home, args.repo, args.user_home)
    if args.json_out:
        write_json(args.json_out, report)
    if args.md_out:
        write_markdown(args.md_out, report)
    if args.format == "json":
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
