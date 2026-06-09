#!/usr/bin/env python3
"""Check README command blocks for runnable sample build commands."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FENCE_RE = re.compile(r"```(?:bash|sh|shell)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def extract_commands(readme: Path) -> list[str]:
    commands: list[str] = []
    text = readme.read_text(encoding="utf-8", errors="replace")
    for block in FENCE_RE.findall(text):
        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith("$ "):
                stripped = stripped[2:].strip()
            if stripped and not stripped.startswith("#"):
                commands.append(stripped)
    return commands


def lint(root: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for makefile in sorted(root.rglob("Makefile")):
        directory = makefile.parent
        readme = directory / "README.md"
        if not readme.exists():
            results.append({"path": directory.relative_to(root).as_posix(), "missing": ["README.md"], "commands": []})
            continue
        commands = extract_commands(readme)
        missing = []
        if not any(command == "make" or command.startswith("make ") for command in commands):
            missing.append("make command")
        if not any(command == "make run" or command.startswith("make run ") for command in commands):
            missing.append("make run command")
        results.append(
            {
                "path": directory.relative_to(root).as_posix(),
                "missing": missing,
                "commands": commands,
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--strict", action="store_true", help="return non-zero when any README fails")
    parser.add_argument("--output", type=Path, help="write JSON report to this path")
    args = parser.parse_args()

    results = lint(args.root)
    payload = {
        "checked": len(results),
        "failed": sum(1 for item in results if item["missing"]),
        "results": results,
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 1 if args.strict and payload["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
