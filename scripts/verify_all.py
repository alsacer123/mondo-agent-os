#!/usr/bin/env python3
"""Run all Mondo Agent OS verification scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("documentation references", "verify_docs.py"),
    ("runtime", "verify_runtime.py"),
    ("mcp", "verify_mcp.py"),
    ("onboarding flow", "verify_onboarding_flow.py"),
]


def main() -> int:
    for label, script_name in CHECKS:
        print(f"== {label} ==", flush=True)
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script_name)],
            cwd=ROOT,
            check=False,
        )
        if result.returncode != 0:
            print(f"{label} verification failed", flush=True)
            return result.returncode

    print("all verifications passed", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
