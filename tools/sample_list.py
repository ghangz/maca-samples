#!/usr/bin/env python3

import argparse
import json
import os


def collect_samples(root):
    samples = []
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [item for item in dirs if item not in (".git", "tools", "tests")]
        if "Makefile" not in files and "README.md" not in files:
            continue
        rel_path = os.path.relpath(current_root, root)
        if rel_path == ".":
            continue
        samples.append({
            "path": rel_path.replace("\\", "/"),
            "category": rel_path.split(os.sep)[0],
            "has_readme": "README.md" in files,
            "build_system": detect_build_system(files),
        })
    samples.sort(key=lambda item: item["path"])
    return samples


def detect_build_system(files):
    if "CMakeLists.txt" in files:
        return "cmake"
    if "Makefile" in files:
        return "make"
    return "unknown"


def main():
    parser = argparse.ArgumentParser(description="List MACA sample directories")
    parser.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))), help="Repository root")
    parser.add_argument("--output", default="", help="Optional JSON output path")
    args = parser.parse_args()

    samples = collect_samples(args.root)
    body = json.dumps(samples, indent=2, ensure_ascii=False)
    print(body)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(body + "\n")


if __name__ == "__main__":
    main()
