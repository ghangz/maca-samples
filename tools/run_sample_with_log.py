#!/usr/bin/env python3
"""Build and run a MACA sample while saving structured validation logs."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path


def _run(command: list[str], cwd: Path) -> dict[str, object]:
    start = time.monotonic()
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": command,
        "returncode": completed.returncode,
        "duration_seconds": round(time.monotonic() - start, 4),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def run_sample(sample_dir: Path, skip_clean: bool) -> dict[str, object]:
    steps: list[dict[str, object]] = []
    if not skip_clean:
        steps.append(_run(["make", "clean"], sample_dir))
    steps.append(_run(["make"], sample_dir))
    if steps[-1]["returncode"] == 0:
        steps.append(_run(["make", "run"], sample_dir))
    return {
        "sample": str(sample_dir),
        "environment": {
            "MACA_PATH": os.environ.get("MACA_PATH", ""),
            "PATH": os.environ.get("PATH", ""),
            "LD_LIBRARY_PATH": os.environ.get("LD_LIBRARY_PATH", ""),
        },
        "steps": steps,
        "success": all(step["returncode"] == 0 for step in steps),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sample_dir", type=Path, help="sample directory containing a Makefile")
    parser.add_argument("--skip-clean", action="store_true", help="do not run make clean first")
    parser.add_argument("--output", type=Path, required=True, help="write validation JSON to this path")
    args = parser.parse_args()

    sample_dir = args.sample_dir.resolve()
    if not (sample_dir / "Makefile").exists():
        raise SystemExit(f"{sample_dir} does not contain a Makefile")
    report = run_sample(sample_dir, args.skip_clean)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
