#!/usr/bin/env python3
"""Generate a shell script for validating one MACA sample."""

from __future__ import annotations

import argparse
from pathlib import Path


def render(sample: str, output_json: str) -> str:
    return f"""#!/usr/bin/env bash
set -euo pipefail
sample_dir="{sample}"
output_json="{output_json}"
mkdir -p "$(dirname "$output_json")"
python tools/run_sample_with_log.py "$sample_dir" --output "$output_json"
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sample")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--script", type=Path, required=True)
    args = parser.parse_args()

    args.script.write_text(render(args.sample, args.output_json), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
