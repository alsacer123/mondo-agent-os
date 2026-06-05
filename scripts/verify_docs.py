#!/usr/bin/env python3
"""Verify local documentation references used by Markdown files."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE_RE = re.compile(
    r"(?<![A-Za-z]:)(?P<path>(?:docs|scripts|skill|templates|src|\.github)/[^\s`\"')\],;:]+)"
)
TRAILING_PUNCTUATION = ".,;:!?"


def markdown_files() -> list[Path]:
    files = [ROOT / "README.md"]
    files.extend(sorted((ROOT / "docs").glob("*.md")))
    files.extend(sorted((ROOT / ".github" / "ISSUE_TEMPLATE").glob("*.md")))
    return [path for path in files if path.exists()]


def normalize_reference(raw: str) -> str:
    reference = raw.strip().rstrip(TRAILING_PUNCTUATION)
    while reference.endswith("/") and len(reference) > 1:
        reference = reference[:-1]
    return reference


def main() -> int:
    missing: list[tuple[Path, int, str]] = []
    checked: set[str] = set()

    for markdown_file in markdown_files():
        content = markdown_file.read_text(encoding="utf-8")
        for line_number, line in enumerate(content.splitlines(), start=1):
            for match in REFERENCE_RE.finditer(line.replace("\\", "/")):
                reference = normalize_reference(match.group("path"))
                target = ROOT / reference
                checked.add(reference)
                if not target.exists():
                    missing.append((markdown_file.relative_to(ROOT), line_number, reference))

    if missing:
        print("missing documentation references:")
        for markdown_file, line_number, reference in missing:
            print(f"- {markdown_file}:{line_number} -> {reference}")
        return 1

    print(f"documentation reference verification passed ({len(checked)} references checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
