"""Core operating spec for Mondo Agent OS."""

from __future__ import annotations

ROOT_FILES = [
    "_索引.md",
    "AGENTS.md",
    "40_Daily/_行动池.md",
    "20_Insights/_README.md",
    "00_Inbox/_README.md",
]

PROJECT_FILES = [
    "_项目规则.md",
    "_总览.md",
    "_当前状态.md",
    "_next.md",
    "决策日志.md",
]

SECRET_PATTERNS = [
    "api_key",
    "apikey",
    "secret_key",
    "private key",
    "BEGIN OPENSSH PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "password=",
    "token=",
]

ROLE_PACKS = {
    "content-personal-brand": {
        "name": "内容生产型个人品牌",
        "description": "For creators who need topic, script, asset, publishing, and review workflows.",
        "project_types": ["选题研究", "脚本生产", "视频制作", "发布复盘", "信任资产"],
        "suggested_files": [
            "topics/选题池.md",
            "system/内容主线.md",
            "assets/品牌设定.md",
            "episodes/README.md",
        ],
    },
    "work-progress": {
        "name": "工作推进型",
        "description": "For professionals who need meeting, reporting, project follow-up, and weekly review workflows.",
        "project_types": ["会议行动", "项目推进", "周报汇总", "向上汇报", "协作等待"],
        "suggested_files": [
            "meetings/会议记录.md",
            "reports/周报.md",
            "stakeholders/协作对象.md",
        ],
    },
}
