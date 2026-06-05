"""First beta run pack generation."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / ".mondo" / "first-beta-run-pack.md"
ISSUE_URL = "https://github.com/alsacer123/mondo-agent-os/issues/new?template=first-beta-run.md"

PACK_SOURCES = [
    ("GitHub issue template", ROOT / ".github" / "ISSUE_TEMPLATE" / "first-beta-run.md"),
    ("Beta user selection", ROOT / "docs" / "beta-user-selection.md"),
    ("Beta user intake template", ROOT / "docs" / "beta-user-intake-template.md"),
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


def build_first_beta_pack() -> str:
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


def write_first_beta_pack(output: Path | None = None) -> Path:
    target = output or DEFAULT_OUTPUT
    if not target.is_absolute():
        target = ROOT / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_first_beta_pack(), encoding="utf-8")
    return target
