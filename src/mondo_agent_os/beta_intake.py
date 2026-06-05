"""First beta candidate intake generation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / ".mondo" / "beta-user-intake.md"
TEMPLATE = ROOT / "docs" / "beta-user-intake-template.md"


def build_beta_user_intake() -> str:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"missing beta user intake template: {TEMPLATE.relative_to(ROOT)}")
    return TEMPLATE.read_text(encoding="utf-8").strip() + "\n"


def write_beta_user_intake(output: Path | None = None) -> Path:
    target = output or DEFAULT_OUTPUT
    if not target.is_absolute():
        target = ROOT / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_beta_user_intake(), encoding="utf-8")
    return target
