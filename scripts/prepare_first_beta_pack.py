#!/usr/bin/env python3
"""Prepare a local host pack for the first real beta run."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mondo_agent_os.beta_pack import DEFAULT_OUTPUT, ISSUE_URL, write_first_beta_pack  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Markdown file to write. Defaults to .mondo/first-beta-run-pack.md.",
    )
    parser.add_argument(
        "--print-path",
        action="store_true",
        help="Print only the generated file path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = write_first_beta_pack(args.output)

    if args.print_path:
        print(output)
    else:
        print(f"first beta run pack written: {output}")
        print(f"issue template: {ISSUE_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
