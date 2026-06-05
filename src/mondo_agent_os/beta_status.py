"""First beta preparation status."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


@dataclass
class BetaArtifact:
    name: str
    path: str
    exists: bool


@dataclass
class BetaStatus:
    status: str
    next_action: str
    artifacts: list[BetaArtifact]


def _artifact(name: str, base: Path, path: Path) -> BetaArtifact:
    try:
        display_path = path.relative_to(base).as_posix()
    except ValueError:
        display_path = str(path)
    return BetaArtifact(name=name, path=display_path, exists=path.exists())


def get_beta_status(root: Path | None = None) -> dict:
    base = root or ROOT
    artifacts = [
        _artifact("first_beta_run_pack", base, base / ".mondo" / "first-beta-run-pack.md"),
        _artifact("candidate_outreach", base, base / ".mondo" / "beta-candidate-outreach.md"),
        _artifact("candidate_intake", base, base / ".mondo" / "beta-user-intake.md"),
    ]
    missing = [item.name for item in artifacts if not item.exists]

    if missing:
        status = "missing_artifacts"
        next_action = "Generate the missing first beta artifacts before contacting a candidate."
    else:
        status = "ready_for_candidate_outreach"
        next_action = "Open .mondo/beta-candidate-outreach.md, list three real candidates, send the light outreach message, then fill .mondo/beta-user-intake.md for the best respondent."

    return asdict(BetaStatus(status=status, next_action=next_action, artifacts=artifacts))
