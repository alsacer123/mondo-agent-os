#!/usr/bin/env python3
"""Prepare a local host pack for the first real beta run."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / ".mondo" / "first-beta-run-pack.md"
ISSUE_URL = "https://github.com/alsacer123/mondo-agent-os/issues/new?template=first-beta-run.md"

PACK_SOURCES = [
    ("GitHub issue template", ROOT / ".github" / "ISSUE_TEMPLATE" / "first-beta-run.md"),
    ("Beta user selection", ROOT / "docs" / "beta-user-selection.md"),
    ("Invitation message", ROOT / "docs" / "beta-invitation-message.md"),
    ("User first day guide", ROOT / "docs" / "user-first-day-guide.md"),
    ("Configuration preflight", ROOT / "docs" / "beta-config-preflight.md"),
    ("Host runbook", ROOT / "docs" / "beta-host-runbook.md"),
    ("Session notes template", ROOT / "docs" / "beta-session-notes-template.md"),
    ("Feedback form", ROOT / "docs" / "beta-feedback-form.md"),
    ("Retro guide", ROOT / "docs" / "beta-retro-guide.md"),
]


def read_source(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"missing pack source: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8").strip()


def build_pack() -> str:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    sections = [
        "# First Beta Run Pack",
        "",
        f"Generated at: {created_at}",
        "",
        "This file is a local execution pack for the first real user beta run.",
        "Use it when GitHub issue creation, browser automation, or network access is not reliable enough during the session.",
        "",
        "## Operator quick path",
        "",
        "1. Open the GitHub issue template link when available:",
        f"   {ISSUE_URL}",
        "2. Run the preflight from the repository root:",
        "   `python scripts/verify_all.py`",
        "3. Send or read the invitation message to the beta user.",
        "4. Host the onboarding with the runbook.",
        "5. Capture notes during the session.",
        "6. Fill the feedback form and retro after the session.",
        "7. Produce exactly one next improvement for the following beta run.",
        "",
        "## GitHub issue fallback",
        "",
        "If the issue cannot be created before the session, do not delay the beta run.",
        "Use the issue template section below as the local checklist, then create the GitHub issue later and paste the session result into it.",
        "",
    ]

    for title, path in PACK_SOURCES:
        relative = path.relative_to(ROOT).as_posix()
        sections.extend(
            [
                "",
                f"## {title}",
                "",
                f"Source: `{relative}`",
                "",
                read_source(path),
                "",
            ]
        )

    return "\n".join(sections).rstrip() + "\n"


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
    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_pack(), encoding="utf-8")

    if args.print_path:
        print(output)
    else:
        print(f"first beta run pack written: {output}")
        print(f"issue template: {ISSUE_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
