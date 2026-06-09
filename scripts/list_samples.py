#!/usr/bin/env python3
"""List buildable MACA samples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def discover_samples(root: Path) -> list[dict[str, str]]:
    samples: list[dict[str, str]] = []
    for makefile in sorted(root.glob("*_*/**/Makefile")):
        sample_dir = makefile.parent
        readme = sample_dir / "README.md"
        samples.append(
            {
                "name": sample_dir.name,
                "category": sample_dir.relative_to(root).parts[0],
                "path": sample_dir.relative_to(root).as_posix(),
                "has_readme": str(readme.is_file()).lower(),
            }
        )
    return samples


def main() -> int:
    parser = argparse.ArgumentParser(description="List buildable MACA sample directories.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="Write machine-readable JSON.")
    args = parser.parse_args()

    root = args.root.resolve()
    samples = discover_samples(root)

    if args.json:
        print(json.dumps({"root": str(root), "count": len(samples), "samples": samples}, indent=2))
    else:
        for sample in samples:
            print(f"{sample['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
