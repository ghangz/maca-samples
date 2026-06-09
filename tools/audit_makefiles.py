#!/usr/bin/env python3
"""Audit MACA sample Makefiles for portable build conventions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def audit_makefile(path: Path, root: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    checks = {
        "defines_maca_path": "MACA_PATH" in text,
        "uses_mxcc": "mxcc" in text.lower() or "MXCC" in text,
        "passes_maca_path": "--maca-path" in text,
        "has_run_target": any(line.startswith("run:") for line in text.splitlines()),
        "has_clean_target": any(line.startswith("clean:") for line in text.splitlines()),
    }
    return {
        "path": path.relative_to(root).as_posix(),
        "checks": checks,
        "missing": [name for name, passed in checks.items() if not passed],
    }


def audit(root: Path) -> list[dict[str, object]]:
    return [audit_makefile(path, root) for path in sorted(root.rglob("Makefile"))]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--strict", action="store_true", help="return non-zero when any check fails")
    parser.add_argument("--output", type=Path, help="write audit JSON to this path")
    args = parser.parse_args()

    results = audit(args.root)
    payload = {
        "makefile_count": len(results),
        "failed_count": sum(1 for item in results if item["missing"]),
        "results": results,
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 1 if args.strict and payload["failed_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
