"""Workspace operations for Mondo Agent OS."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

from .spec import PROJECT_FILES, ROOT_FILES, SECRET_PATTERNS
from .templates import DAILY_TEMPLATE, PROJECT_TEMPLATES, ROOT_TEMPLATES


@dataclass
class ProjectReport:
    path: str
    missing_files: list[str]


@dataclass
class DoctorReport:
    root: str
    missing_root_files: list[str]
    projects_checked: int
    projects_with_missing_files: list[ProjectReport]
    secret_warnings: list[str]
    status: str


def write_if_missing(path: Path, content: str, force: bool = False) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return "kept"
    path.write_text(content, encoding="utf-8")
    return "written"


def init_workspace(root: Path, project: str, force: bool = False) -> list[str]:
    root = root.expanduser().resolve()
    today = date.today().isoformat()
    results: list[str] = []

    for rel, content in ROOT_TEMPLATES.items():
        results.append(f"{write_if_missing(root / rel, content, force)}: {rel}")

    daily_rel = Path("40_Daily") / "days" / today[:4] / f"{today}.md"
    results.append(
        f"{write_if_missing(root / daily_rel, DAILY_TEMPLATE.format(today=today), force)}: {daily_rel}"
    )

    project_root = root / "30_Projects" / project
    for rel, content in PROJECT_TEMPLATES.items():
        file_rel = Path("30_Projects") / project / rel
        results.append(f"{write_if_missing(root / file_rel, content, force)}: {file_rel}")

    return results


def find_projects(root: Path) -> list[Path]:
    projects_root = root / "30_Projects"
    if not projects_root.exists():
        return []

    projects: list[Path] = []
    for rules in projects_root.rglob("_项目规则.md"):
        projects.append(rules.parent)
    return sorted(projects)


def scan_workspace(root: Path) -> dict:
    root = root.expanduser().resolve()
    projects = []
    for project in find_projects(root):
        projects.append(
            {
                "path": str(project.relative_to(root)),
                "has_next": (project / "_next.md").exists(),
                "has_status": (project / "_当前状态.md").exists(),
                "has_decision_log": (project / "决策日志.md").exists(),
            }
        )
    return {
        "root": str(root),
        "root_files": {rel: (root / rel).exists() for rel in ROOT_FILES},
        "projects": projects,
        "daily_action_pool": str(Path("40_Daily") / "_行动池.md"),
    }


def build_live_state(root: Path) -> dict:
    root = root.expanduser().resolve()
    today = date.today().isoformat()
    watched_files = [
        root / "40_Daily" / "_行动池.md",
        root / "40_Daily" / "days" / today[:4] / f"{today}.md",
    ]
    for project in find_projects(root):
        watched_files.extend(
            [
                project / "_next.md",
                project / "_当前状态.md",
            ]
        )

    files = []
    for path in watched_files:
        if not path.exists():
            continue
        stat = path.stat()
        files.append(
            {
                "path": str(path.relative_to(root)),
                "modified_at": int(stat.st_mtime),
                "size": stat.st_size,
                "preview": extract_preview(path),
            }
        )

    return {
        "root": str(root),
        "generated_at": int(time.time()),
        "today": today,
        "files": files,
    }


def write_live_state(root: Path) -> Path:
    root = root.expanduser().resolve()
    state = build_live_state(root)
    output = root / ".mondo" / "live-state.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(to_json(state), encoding="utf-8")
    return output


def export_agent_context(root: Path) -> Path:
    root = root.expanduser().resolve()
    state = build_live_state(root)
    output = root / ".mondo" / "agent-context.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Mondo Agent Context",
        "",
        f"- root: `{state['root']}`",
        f"- today: `{state['today']}`",
        "",
        "## Read First",
        "",
        "1. `_索引.md`",
        "2. `40_Daily/_行动池.md`",
        "3. today's Daily",
        "4. project `_项目规则.md` and `_next.md` when acting inside a project",
        "",
        "## Live Files",
        "",
    ]
    for file in state["files"]:
        lines.append(f"### {file['path']}")
        lines.append("")
        if file["preview"]:
            lines.append(file["preview"])
        else:
            lines.append("(no preview)")
        lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def extract_preview(path: Path, max_lines: int = 12) -> str:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return ""
    meaningful = [line for line in lines if line.strip()]
    return "\n".join(meaningful[:max_lines])


def doctor_workspace(root: Path) -> DoctorReport:
    root = root.expanduser().resolve()
    missing_root = [rel for rel in ROOT_FILES if not (root / rel).exists()]

    project_reports: list[ProjectReport] = []
    projects = find_projects(root)
    for project in projects:
        missing = [rel for rel in PROJECT_FILES if not (project / rel).exists()]
        if missing:
            project_reports.append(
                ProjectReport(path=str(project.relative_to(root)), missing_files=missing)
            )

    secret_warnings = scan_secret_warnings(root)
    status = "ok"
    if missing_root or project_reports or secret_warnings:
        status = "needs_attention"

    return DoctorReport(
        root=str(root),
        missing_root_files=missing_root,
        projects_checked=len(projects),
        projects_with_missing_files=project_reports,
        secret_warnings=secret_warnings,
        status=status,
    )


def scan_secret_warnings(root: Path) -> list[str]:
    warnings: list[str] = []
    skip_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__"}
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".json", ".yaml", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lowered = text.lower()
        for pattern in SECRET_PATTERNS:
            if pattern.lower() in lowered:
                warnings.append(str(path.relative_to(root)))
                break
    return warnings[:50]


def route_input(text: str) -> dict:
    lowered = text.lower()
    if any(word in lowered for word in ["今天", "马上", "now", "today", "刚刚", "临时"]):
        target = "daily"
        reason = "Looks executable today or time-sensitive."
    elif any(word in lowered for word in ["等待", "以后", "也许", "灵感", "想法", "backlog"]):
        target = "action_pool"
        reason = "Looks like future, waiting, or loose input."
    elif any(word in lowered for word in ["复盘", "方法", "sop", "原则", "经验", "沉淀"]):
        target = "insights"
        reason = "Looks reusable beyond one project."
    elif any(word in lowered for word in ["项目", "客户", "交付", "版本", "发布", "开发"]):
        target = "project"
        reason = "Looks tied to a project or delivery."
    else:
        target = "inbox"
        reason = "No stable destination detected."
    return {"target": target, "reason": reason, "input": text}


def to_json(data: object) -> str:
    if hasattr(data, "__dataclass_fields__"):
        data = asdict(data)
    return json.dumps(data, ensure_ascii=False, indent=2)
