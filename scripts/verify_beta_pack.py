#!/usr/bin/env python3
"""Verify the first beta run pack can be generated."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_MARKERS = [
    "# First Beta Run Pack",
    "GitHub issue template",
    "Beta user selection",
    "Invitation message",
    "User first day guide",
    "Configuration preflight",
    "Host runbook",
    "Session notes template",
    "Feedback form",
    "Retro guide",
    "https://github.com/alsacer123/mondo-agent-os/issues/new?template=first-beta-run.md",
]


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "first-beta-run-pack.md"
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "prepare_first_beta_pack.py"),
                "--output",
                str(output),
            ],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            print(result.stdout, end="")
            print(result.stderr, end="")
            return result.returncode

        content = output.read_text(encoding="utf-8")
        missing = [marker for marker in REQUIRED_MARKERS if marker not in content]
        if missing:
            print("first beta run pack is missing required markers:")
            for marker in missing:
                print(f"- {marker}")
            return 1

    print("first beta run pack verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
