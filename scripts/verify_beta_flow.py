#!/usr/bin/env python3
"""Verify the first beta onboarding flow from the customer outcome checklist."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mondo_agent_os.onboarding import (  # noqa: E402
    collect_identity,
    collect_projects,
    confirm_onboarding,
    onboarding_status,
    start_onboarding,
)
from mondo_agent_os.workspace import export_agent_context  # noqa: E402


IDENTITY_NOTES = """
我希望未来 3-6 个月把自己的工作从每天临时反应，变成一个能持续推进的系统。
最重要的方向是个人品牌、客户交付和学习成长。
我最不想继续硬扛的是：所有项目都在脑子里，每次和 AI 聊都要重新解释背景。
AI 可以帮我整理项目、生成下一步、做早间整理和晚间收口。
AI 不能自动发送客户消息、不能写入密钥、不能替我做最终商业承诺。
"""

PROJECT_NOTES = """
我现在有三个真实项目。
第一个是个人品牌内容系统：正在写一篇关于 AI 工作系统的长文，下一步是整理大纲。
第二个是客户交付：客户下周要看方案，下一步是整理方案大纲给客户确认。
第三个是学习成长：我在练习口播表达，当前只是保活项目，每天 15 分钟练习。
本周主线是个人品牌内容系统和客户交付；学习成长只保活。
"""


REQUIRED_FILES = [
    "_Identity/长期方向.md",
    "_Identity/定位.md",
    "_Identity/内容原则.md",
    "40_Daily/_行动池.md",
    "30_Projects/个人工作系统初始化/_项目规则.md",
    "30_Projects/个人工作系统初始化/_总览.md",
    "30_Projects/个人工作系统初始化/_当前状态.md",
    "30_Projects/个人工作系统初始化/_next.md",
    "30_Projects/个人工作系统初始化/决策日志.md",
]


def assert_contains(path: Path, expected: str) -> None:
    text = path.read_text(encoding="utf-8")
    if expected not in text:
        raise AssertionError(f"{path} does not contain expected text: {expected}")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "beta-work-os"

        started = start_onboarding(workspace)
        assert started["phase"] == "collecting_identity", started

        identity = collect_identity(workspace, IDENTITY_NOTES)
        assert identity["phase"] == "collecting_projects", identity

        projects = collect_projects(workspace, PROJECT_NOTES)
        assert projects["phase"] == "draft_ready", projects
        assert "个人品牌内容系统" in projects["draft"]["project_intake"], projects

        confirmed = confirm_onboarding(workspace)
        assert confirmed["phase"] == "active_daily_flow", confirmed

        status = onboarding_status(workspace)
        assert status["phase"] == "active_daily_flow", status
        assert status["confirmed"] is True, status

        missing = [rel for rel in REQUIRED_FILES if not (workspace / rel).exists()]
        if missing:
            raise AssertionError(f"Missing expected beta output files: {missing}")

        today_files = list((workspace / "40_Daily" / "days").rglob("*.md"))
        if not today_files:
            raise AssertionError("Missing generated Daily file")

        assert_contains(workspace / "_Identity" / "长期方向.md", "个人品牌")
        assert_contains(workspace / "30_Projects" / "个人工作系统初始化" / "_总览.md", "客户交付")
        assert_contains(workspace / "40_Daily" / "_行动池.md", "确认初始化草稿")

        context_path = export_agent_context(workspace)
        assert context_path.exists(), context_path
        assert_contains(context_path, "Mondo Agent Context")

        report = {
            "workspace": str(workspace),
            "required_files_checked": len(REQUIRED_FILES),
            "daily_files": [str(path.relative_to(workspace)) for path in today_files],
            "phase": status["phase"],
            "confirmed": status["confirmed"],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        print("beta flow verification passed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
