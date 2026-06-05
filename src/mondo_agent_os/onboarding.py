"""Onboarding flow for turning a blank folder into a running work OS."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import date
from pathlib import Path
from typing import Any

from .workspace import append_markdown, write_if_missing

STATE_PATH = Path(".mondo") / "onboarding-state.json"

PHASES = [
    "not_initialized",
    "collecting_identity",
    "collecting_projects",
    "draft_ready",
    "active_daily_flow",
]


IDENTITY_PROMPTS = [
    "你长期想把工作和生活变成什么样？",
    "未来 3-6 个月，最重要的 1-3 个方向是什么？",
    "你现在最不想继续用蛮力硬扛的工作是什么？",
    "你希望 AI 能帮你接住哪些事情？哪些事情绝对不能自动做？",
]

PROJECT_PROMPTS = [
    "请一次性说出你现在手上所有正在推进、等待中、暂停但还重要的项目。",
    "每个项目现在做到哪一步？请尽量说事实，不用整理成漂亮文字。",
    "每个项目当前最明确的下一步是什么？如果不知道，也直接说不知道。",
    "哪些项目是本周主线？哪些只是保活？哪些应该先暂停？",
]


@dataclass
class OnboardingState:
    phase: str = "collecting_identity"
    created_at: str = field(default_factory=lambda: date.today().isoformat())
    updated_at: str = field(default_factory=lambda: date.today().isoformat())
    identity_notes: list[str] = field(default_factory=list)
    project_notes: list[str] = field(default_factory=list)
    confirmed: bool = False


def state_file(root: Path) -> Path:
    return root.expanduser().resolve() / STATE_PATH


def load_state(root: Path) -> OnboardingState:
    path = state_file(root)
    if not path.exists():
        return OnboardingState()
    data = json.loads(path.read_text(encoding="utf-8"))
    return OnboardingState(**data)


def save_state(root: Path, state: OnboardingState) -> Path:
    state.updated_at = date.today().isoformat()
    path = state_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(state), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def start_onboarding(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    state = OnboardingState()
    save_state(root, state)
    return {
        "phase": state.phase,
        "next_questions": IDENTITY_PROMPTS,
        "message": "Start by collecting identity, long-term direction, current friction, and AI boundaries.",
    }


def collect_identity(root: Path, notes: str) -> dict[str, Any]:
    state = load_state(root)
    state.identity_notes.append(notes.strip())
    state.phase = "collecting_projects"
    save_state(root, state)
    return {
        "phase": state.phase,
        "next_questions": PROJECT_PROMPTS,
        "message": "Identity notes captured. Now collect all active, waiting, and paused projects.",
    }


def collect_projects(root: Path, notes: str) -> dict[str, Any]:
    state = load_state(root)
    state.project_notes.append(notes.strip())
    state.phase = "draft_ready"
    save_state(root, state)
    return {
        "phase": state.phase,
        "draft": build_draft(state),
        "message": "Project notes captured. Review the draft with the user before writing workspace files.",
    }


def onboarding_status(root: Path) -> dict[str, Any]:
    state = load_state(root)
    return {
        "phase": state.phase,
        "created_at": state.created_at,
        "updated_at": state.updated_at,
        "identity_notes_count": len(state.identity_notes),
        "project_notes_count": len(state.project_notes),
        "confirmed": state.confirmed,
        "next_questions": next_questions_for_phase(state.phase),
        "draft": build_draft(state) if state.phase in {"draft_ready", "active_daily_flow"} else None,
    }


def confirm_onboarding(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    state = load_state(root)
    if not state.identity_notes or not state.project_notes:
        raise ValueError("Onboarding needs both identity notes and project notes before confirmation.")

    draft = build_draft(state)
    written: list[str] = []
    written.extend(write_identity_files(root, draft))
    written.extend(write_project_intake_files(root, draft))
    written.extend(write_daily_flow_files(root, draft))

    state.phase = "active_daily_flow"
    state.confirmed = True
    save_state(root, state)

    return {
        "phase": state.phase,
        "written": written,
        "message": "Workspace confirmed. Start morning planning and evening closeout from now on.",
    }


def build_draft(state: OnboardingState) -> dict[str, Any]:
    identity_text = "\n\n".join(state.identity_notes).strip()
    project_text = "\n\n".join(state.project_notes).strip()
    return {
        "identity_summary": identity_text or "尚未采集长期方向。",
        "project_intake": project_text or "尚未采集项目。",
        "suggested_project_name": "个人工作系统初始化",
        "first_daily_action": "确认初始化草稿，并把当前项目拆成可执行的唯一下一步。",
        "operating_mode": "先建立工作现场，再进入每日早间整理、白天推进、晚间收口。",
    }


def next_questions_for_phase(phase: str) -> list[str]:
    if phase in {"not_initialized", "collecting_identity"}:
        return IDENTITY_PROMPTS
    if phase == "collecting_projects":
        return PROJECT_PROMPTS
    if phase == "draft_ready":
        return [
            "这份长期方向是否像你？",
            "项目有没有漏掉、分错或该暂停的？",
            "哪些项目应该成为本周主线？",
            "确认后是否写入工作区？",
        ]
    if phase == "active_daily_flow":
        return [
            "早间整理：今天从行动池和项目下一步里抽哪几件？",
            "晚间收口：完成了什么，未完成回流哪里，项目状态要不要更新？",
        ]
    return []


def write_identity_files(root: Path, draft: dict[str, Any]) -> list[str]:
    identity_root = root / "_Identity"
    files = {
        "_Identity/长期方向.md": f"# 长期方向\n\n{draft['identity_summary']}\n",
        "_Identity/定位.md": "# 定位\n\n> 初始化阶段生成，后续需要用户继续校准。\n\n" + draft["identity_summary"] + "\n",
        "_Identity/内容原则.md": "# 内容原则与工作原则\n\n- 系统 > 单点工具。\n- 真实工作流 > 漂亮模板。\n- 每次只推进一个清晰下一步。\n",
    }
    written = []
    identity_root.mkdir(parents=True, exist_ok=True)
    for rel, content in files.items():
        result = write_if_missing(root / rel, content, force=False)
        written.append(f"{result}: {rel}")
    return written


def write_project_intake_files(root: Path, draft: dict[str, Any]) -> list[str]:
    project = Path("30_Projects") / draft["suggested_project_name"]
    files = {
        project / "_项目规则.md": "# 项目规则\n\n- 先基于用户确认过的项目现场推进。\n- 不读取无关项目。\n- 写入前先说明写入位置和内容。\n",
        project / "_总览.md": f"# 项目总览\n\n## 初始项目口述\n\n{draft['project_intake']}\n",
        project / "_当前状态.md": "# 当前状态\n\n## 初始化判断\n\n- 已完成初始项目口述采集，等待继续拆分具体项目文件。\n",
        project / "_next.md": f"# 下一步\n\n## 当前下一步\n\n状态：待做\n\n动作：{draft['first_daily_action']}\n\n完成标志：用户确认主线项目和第一个可执行动作。\n\n## 已完成归档\n",
        project / "决策日志.md": "# 决策日志\n\n- 初始化阶段：先把用户口述收成一个项目现场，再逐步拆分到具体项目。\n",
    }
    written = []
    for rel, content in files.items():
        result = write_if_missing(root / rel, content, force=False)
        written.append(f"{result}: {rel}")
    return written


def write_daily_flow_files(root: Path, draft: dict[str, Any]) -> list[str]:
    today = date.today().isoformat()
    written = []
    action_pool = root / "40_Daily" / "_行动池.md"
    daily = root / "40_Daily" / "days" / today[:4] / f"{today}.md"

    action_pool.parent.mkdir(parents=True, exist_ok=True)
    if not action_pool.exists():
        action_pool.write_text("# 行动池\n\n## 下一步动作\n\n## 等待中\n\n## 将来也许\n\n## 灵感输入\n", encoding="utf-8")
        written.append("written: 40_Daily/_行动池.md")
    append_markdown(root, "40_Daily/_行动池.md", f"- [ ] {draft['first_daily_action']}", "初始化下一步")
    written.append("appended: 40_Daily/_行动池.md")

    daily.parent.mkdir(parents=True, exist_ok=True)
    if not daily.exists():
        daily.write_text(
            f"# {today}\n\n## 今日任务池\n\n- [ ] {draft['first_daily_action']}\n\n## 晚间收口\n\n- 今天完成：\n- 未完成 / 卡点：\n- 明天第一步：\n",
            encoding="utf-8",
        )
        written.append(f"written: 40_Daily/days/{today[:4]}/{today}.md")
    return written
