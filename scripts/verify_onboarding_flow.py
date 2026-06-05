#!/usr/bin/env python3
"""Verify the guided onboarding flow can build a working Mondo workspace."""

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
    start_onboarding,
)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "work-os"

        started = start_onboarding(workspace)
        assert started["phase"] == "collecting_identity", started

        identity = collect_identity(
            workspace,
            "我想让 AI 能持续接住个人工作现场，不想每次都重新解释背景。未来 3-6 个月要把内容输出和客户交付两条线稳定下来。",
        )
        assert identity["phase"] == "collecting_projects", identity

        projects = collect_projects(
            workspace,
            "我现在有两个项目：个人品牌内容系统和客户交付。个人品牌要继续写下一篇长文，客户交付要下周给方案。",
        )
        assert projects["phase"] == "draft_ready", projects

        confirmed = confirm_onboarding(workspace)
        assert confirmed["phase"] == "active_daily_flow", confirmed

        required = [
            workspace / "_Identity" / "长期方向.md",
            workspace / "40_Daily" / "_行动池.md",
            workspace / "30_Projects" / "个人工作系统初始化" / "_项目规则.md",
            workspace / "30_Projects" / "个人工作系统初始化" / "_总览.md",
            workspace / "30_Projects" / "个人工作系统初始化" / "_当前状态.md",
            workspace / "30_Projects" / "个人工作系统初始化" / "_next.md",
            workspace / "30_Projects" / "个人工作系统初始化" / "决策日志.md",
        ]
        missing = [str(path.relative_to(workspace)) for path in required if not path.exists()]
        if missing:
            raise AssertionError(f"Missing expected onboarding output files: {missing}")

        daily_files = list((workspace / "40_Daily" / "days").glob("*/*.md"))
        if not daily_files:
            raise AssertionError("Missing daily file")

        print(
            json.dumps(
                {
                    "workspace": str(workspace),
                    "required_files_checked": len(required),
                    "daily_files": [str(path.relative_to(workspace)) for path in daily_files],
                    "phase": confirmed["phase"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )

    print("onboarding flow verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
