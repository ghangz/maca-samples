#!/usr/bin/env python3
"""Check that buildable MACA samples have local README files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def find_missing_readmes(root: Path) -> list[Path]:
    missing: list[Path] = []
    for makefile in sorted(root.glob("*_*/**/Makefile")):
        sample_dir = makefile.parent
        if not (sample_dir / "README.md").is_file():
            missing.append(sample_dir.relative_to(root))
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate README coverage for MACA samples.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    root = args.root.resolve()
    missing = find_missing_readmes(root)
    if missing:
        print("Samples missing README.md:", file=sys.stderr)
        for path in missing:
            print(f"  {path.as_posix()}", file=sys.stderr)
        return 1

    print("All buildable samples have README.md files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
