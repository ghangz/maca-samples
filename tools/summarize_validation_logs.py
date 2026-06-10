#!/usr/bin/env python3
"""Summarize per-sample validation JSON logs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def summarize(log_dir: Path) -> dict[str, object]:
    records = []
    for path in sorted(log_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            records.append(
                {
                    "path": path.name,
                    "sample": data.get("sample", ""),
                    "success": bool(data.get("success")),
                }
            )
        except (json.JSONDecodeError, OSError) as exc:
            records.append(
                {
                    "path": path.name,
                    "sample": "",
                    "success": False,
                    "error": str(exc),
                }
            )
    return {
        "log_count": len(records),
        "passed": sum(1 for item in records if item["success"]),
        "failed": sum(1 for item in records if not item["success"]),
        "logs": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if not args.log_dir.is_dir():
        parser.error(f"log directory does not exist: {args.log_dir}")

    text = json.dumps(summarize(args.log_dir), indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
