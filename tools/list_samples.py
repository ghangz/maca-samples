#!/usr/bin/env python3
"""Build a machine-readable inventory of MACA sample directories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE_SUFFIXES = {".cpp", ".cc", ".c", ".cu", ".maca"}


def _has_make_target(makefile: Path, target: str) -> bool:
    if not makefile.exists():
        return False
    for line in makefile.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(f"{target}:"):
            return True
    return False


def discover(root: Path) -> list[dict[str, object]]:
    samples: list[dict[str, object]] = []
    for makefile in sorted(root.rglob("Makefile")):
        directory = makefile.parent
        sources = sorted(
            path.name for path in directory.iterdir() if path.is_file() and path.suffix in SOURCE_SUFFIXES
        )
        if not sources:
            continue
        samples.append(
            {
                "path": directory.relative_to(root).as_posix(),
                "sources": sources,
                "has_readme": (directory / "README.md").exists(),
                "has_run_target": _has_make_target(makefile, "run"),
                "has_clean_target": _has_make_target(makefile, "clean"),
            }
        )
    return samples


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--output", type=Path, help="write JSON inventory to this path")
    args = parser.parse_args()

    payload = {"sample_count": len(discover(args.root)), "samples": discover(args.root)}
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
