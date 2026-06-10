#!/usr/bin/env python3
"""Check README command blocks for runnable sample build commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SKIP_DIRS = {"build", "out", "venv", ".venv", "__pycache__"}


def extract_commands(readme: Path) -> list[str]:
    commands: list[str] = []
    text = readme.read_text(encoding="utf-8", errors="replace")
    blocks: list[str] = []
    current_block: list[str] = []
    in_shell_block = False
    active = False
    for raw_line in text.splitlines():
        stripped_line = raw_line.strip()
        if stripped_line.startswith("```"):
            marker = stripped_line[3:].strip().lower()
            if active:
                if in_shell_block:
                    blocks.append("\n".join(current_block))
                current_block = []
                active = False
                in_shell_block = False
            else:
                active = True
                in_shell_block = marker in {"", "bash", "sh", "shell"}
            continue
        if active and in_shell_block:
            current_block.append(raw_line)

    for block in blocks:
        current: list[str] = []
        for line in block.splitlines():
            stripped = line.strip()
            if stripped.startswith("$ "):
                stripped = stripped[2:].strip()
            if stripped and not stripped.startswith("#"):
                if stripped.endswith("\\"):
                    current.append(stripped[:-1].rstrip())
                    continue
                if current:
                    current.append(stripped)
                    commands.append(" ".join(part for part in current if part))
                    current = []
                else:
                    commands.append(stripped)
        if current:
            commands.append(" ".join(part for part in current if part))
    return commands


def lint(root: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for makefile in sorted(root.rglob("Makefile")):
        parts = makefile.relative_to(root).parts[:-1]
        if any(part.startswith(".") or part in SKIP_DIRS for part in parts):
            continue
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
