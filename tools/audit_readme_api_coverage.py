#!/usr/bin/env python3
"""Check that sample READMEs mention MACA APIs used by source files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


API_RE = re.compile(r"\bmc[A-Z][A-Za-z0-9_]+\b")


def audit(root: Path) -> dict[str, object]:
    results = []
    for makefile in sorted(root.rglob("Makefile")):
        directory = makefile.parent
        source_files = [
            path
            for pattern in ("*.cpp", "*.cu", "*.h", "*.hpp")
            for path in sorted(directory.glob(pattern))
        ]
        source_text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace") for path in source_files
        )
        readme = directory / "README.md"
        readme_text = readme.read_text(encoding="utf-8", errors="replace") if readme.exists() else ""
        used = sorted(set(API_RE.findall(source_text)))
        documented = set(API_RE.findall(readme_text))
        missing = [api for api in used if api not in documented]
        results.append(
            {
                "path": directory.relative_to(root).as_posix(),
                "used_apis": used,
                "missing_from_readme": missing,
            }
        )
    return {"sample_count": len(results), "samples_with_missing_apis": sum(1 for item in results if item["missing_from_readme"]), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    text = json.dumps(audit(args.root), indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
