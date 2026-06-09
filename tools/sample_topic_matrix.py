#!/usr/bin/env python3
"""Build a topic matrix for MACA sample validation planning."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TOPICS = {
    "memory": ("mcMalloc", "mcMemcpy", "mcMemset", "mcMallocManaged", "mcMallocHost"),
    "graph": ("mcGraph", "mcStreamBeginCapture", "mcStreamEndCapture"),
    "multi_gpu": ("mcGetDeviceCount", "mcSetDevice", "mccl", "MPI"),
    "ipc": ("mcIpc", "mcDeviceCanAccessPeer"),
    "profiler": ("mcProfilerStart", "mcProfilerStop"),
}


def matrix(root: Path) -> dict[str, object]:
    samples = []
    for makefile in sorted(root.rglob("Makefile")):
        directory = makefile.parent
        text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in directory.glob("*.*") if path.suffix in {".cpp", ".md"})
        topics = [name for name, needles in TOPICS.items() if any(needle in text for needle in needles)]
        samples.append({"path": directory.relative_to(root).as_posix(), "topics": topics})
    return {"sample_count": len(samples), "samples": samples}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    text = json.dumps(matrix(args.root), indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
