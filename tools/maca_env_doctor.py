#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
from dataclasses import dataclass, asdict


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def run_command(command, timeout):
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return False, "command not found"
    except subprocess.TimeoutExpired:
        return False, "command timed out"

    detail = completed.stdout.strip() or completed.stderr.strip() or ("exit code %d" % completed.returncode)
    return completed.returncode == 0, detail


def inspect_maca_home(path):
    if not path:
        return CheckResult("MACA_HOME", False, "environment variable is not set")
    if not os.path.isdir(path):
        return CheckResult("MACA_HOME", False, "path does not exist: %s" % path)

    missing = []
    for child in ("bin", "include"):
        if not os.path.exists(os.path.join(path, child)):
            missing.append(child)
    if not os.path.exists(os.path.join(path, "lib")) and not os.path.exists(os.path.join(path, "lib64")):
        missing.append("lib/lib64")

    if missing:
        return CheckResult("MACA_HOME", False, "missing subdirectories: %s" % ", ".join(missing))
    return CheckResult("MACA_HOME", True, path)


def inspect_binary(name):
    path = shutil.which(name)
    if path is None:
        return CheckResult(name, False, "binary not found in PATH")
    return CheckResult(name, True, path)


def build_report(timeout):
    report = {
        "checks": [],
    }

    report["checks"].append(asdict(inspect_maca_home(os.environ.get("MACA_HOME"))))
    for binary in ("make", "cmake", "python3", "maca-smi"):
        report["checks"].append(asdict(inspect_binary(binary)))

    maca_smi_path = shutil.which("maca-smi")
    if maca_smi_path is None:
        maca_home = os.environ.get("MACA_HOME")
        if maca_home:
            fallback = os.path.join(maca_home, "bin", "maca-smi")
            if os.path.exists(fallback):
                maca_smi_path = fallback

    if maca_smi_path is not None:
        ok, detail = run_command([maca_smi_path, "-L"], timeout)
    else:
        ok, detail = False, "maca-smi command not found"
    report["checks"].append(asdict(CheckResult("maca-smi -L", ok, detail)))
    return report


def main():
    parser = argparse.ArgumentParser(description="Inspect the local MACA sample environment")
    parser.add_argument("--timeout", type=int, default=5, help="Command timeout in seconds")
    parser.add_argument("--output", type=str, default="", help="Optional JSON output path")
    args = parser.parse_args()

    report = build_report(args.timeout)
    body = json.dumps(report, indent=2, ensure_ascii=False)
    print(body)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(body + "\n")

    failed = any(not item["ok"] for item in report["checks"])
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
