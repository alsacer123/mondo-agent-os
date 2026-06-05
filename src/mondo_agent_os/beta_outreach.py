"""First beta candidate outreach generation."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / ".mondo" / "beta-candidate-outreach.md"
TEMPLATE = ROOT / "docs" / "beta-candidate-outreach.md"


def build_beta_candidate_outreach() -> str:
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"missing beta candidate outreach template: {TEMPLATE.relative_to(ROOT)}")
    return TEMPLATE.read_text(encoding="utf-8").strip() + "\n"


def write_beta_candidate_outreach(output: Path | None = None) -> Path:
    target = output or DEFAULT_OUTPUT
    if not target.is_absolute():
        target = ROOT / target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_beta_candidate_outreach(), encoding="utf-8")
    return target
