#!/usr/bin/env python3
"""Audit sample Makefiles for common automation targets."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TARGET_RE = re.compile(r"^([A-Za-z0-9_.-]+)\s*:(?!=)", re.MULTILINE)
REQUIRED = ("all", "run", "clean")


def audit(root: Path) -> dict[str, object]:
    root = root.resolve()
    results = []
    for makefile in sorted(root.rglob("Makefile")):
        targets = sorted(set(TARGET_RE.findall(makefile.read_text(encoding="utf-8", errors="replace"))))
        missing = [target for target in REQUIRED if target not in targets]
        results.append({"path": makefile.parent.relative_to(root).as_posix(), "targets": targets, "missing": missing})
    return {"makefile_count": len(results), "failed_count": sum(1 for item in results if item["missing"]), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = audit(args.root)
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 1 if args.strict and report["failed_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
