#!/usr/bin/env python3
"""Initialize an AI Personal Work OS folder structure."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


FILES = {
    "_索引.md": """---
用途：AI 进入工作区时先读的全局索引
更新频率：低频，只在全局结构变化时更新
---

# 工作区索引

## 全局红线

- 不要无差别读取整个工作区。
- 工作区只保存状态、结论、决策、路径和可复用方法。
- 大文件、缓存、依赖和批量输出物放外部工作区。
- 不要把 key、token、密码、私钥、服务器 IP、完整登录命令写进工作区。
- 不确定归属、是否删除、是否覆盖时，先问人。

## 按需读取

| 需要 | 读取 |
|---|---|
| 执行具体项目 | 进入项目目录，先读 `_项目规则.md`，再读 `_next.md` |
| 判断项目现状 | 项目的 `_当前状态.md` |
| 查项目背景 | 项目的 `_总览.md` |
| 查重大取舍 | 项目的 `决策日志.md` |
| 整理今日动作 | `40_Daily/_行动池.md` 和当天 Daily |

## 写回规则

- 下一步变化写项目 `_next.md`。
- 状态变化写项目 `_当前状态.md`。
- 重大转向写项目 `决策日志.md`。
- 可复用经验写 `20_Insights/`。
- 跨项目动作、等待事项、将来也许写 `40_Daily/_行动池.md`。
""",
    "AGENTS.md": """# AGENTS.md

处理本工作区任务时：

1. 从工作区根目录进入时，先读 `_索引.md`。
2. 从具体项目进入时，先读该项目 `_项目规则.md`。
3. 只处理用户指定的文件、目录或项目。
4. 不修改、创建、删除无关文件。
5. 不把密钥、token、密码、私钥、服务器 IP、客户隐私或完整登录命令写进工作区。
6. 大输出物放外部工作区，不放进知识库。
7. 完成任务后，把结果写回项目 `_next.md` 或 `_当前状态.md`；重大转向写 `决策日志.md`。
""",
    "40_Daily/_行动池.md": """# 行动池

> 跨项目动作、等待事项、灵感和将来也许。这里不是今日任务清单。

## 今日可抽取

- [ ] 

## 等待中

- [ ] 

## 将来也许

- [ ] 

## 灵感输入

- 

## 回流规则

- 今天确定要做的，移动到当天 Daily。
- 跨天未完成但仍重要的，回流到行动池。
- 已经属于具体项目的，写回对应项目 `_next.md`。
""",
    "20_Insights/_README.md": """# Insights

这里存放可复用方法、复盘结论、SOP 和长期判断。

不要把日常流水账写进这里。
""",
    "00_Inbox/_README.md": """# Inbox

只放暂时无法判断归属的输入。

定期清空：归入项目、行动池、Daily 或 Insights。
""",
}


PROJECT_FILES = {
    "_项目规则.md": """---
用途：项目级 AI 协作规则
更新频率：低频
---

# 项目规则

## 本项目红线

- 不读取无关项目文件。
- 不创建、删除、移动无关文件。
- 不把密钥、token、密码、私钥、服务器 IP、客户隐私、完整登录命令写进项目。
- 大文件、导出物、缓存、依赖和批量输出放到外部工作区。

## 按需读取

| 要做什么 | 读什么 |
|---|---|
| 继续当前动作 | `_next.md` |
| 判断现状 | `_当前状态.md` |
| 查背景和长期目标 | `_总览.md` |
| 查重大取舍 | `决策日志.md` |

## 写回

- 下一步变化：`_next.md`
- 状态变化：`_当前状态.md`
- 重大转向：`决策日志.md`
""",
    "_总览.md": """# 项目总览

## 定位

这个项目负责什么，不负责什么。

## 当前目标

- 

## 关键入口

- `_项目规则.md`
- `_当前状态.md`
- `_next.md`
- `决策日志.md`
""",
    "_当前状态.md": """# 当前状态

## 一句话状态


## 已确认判断

- 

## 当前资产

- 

## 当前风险

- 
""",
    "_next.md": """---
用途：当前唯一下一步
规则：顶部只保留一条半天会话级动作；完成后归档到底部，再写新的唯一下一步
---

# 下一步

更新时间：YYYY-MM-DD

## 当前下一步

状态：待做

动作：

完成标志：

备注：

## 已完成归档
""",
    "决策日志.md": """# 决策日志

> 只记录重大转向、不可逆取舍、长期规则变化。

---
""",
}


def write_if_missing(path: Path, content: str, force: bool) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return "kept"
    path.write_text(content, encoding="utf-8")
    return "written"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Target workspace root")
    parser.add_argument("--project", default="示例AI赋能项目", help="Initial project name")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    today = date.today().isoformat()
    results: list[str] = []

    for rel, content in FILES.items():
        result = write_if_missing(root / rel, content, args.force)
        results.append(f"{result}: {rel}")

    daily = root / "40_Daily" / "days" / today[:4] / f"{today}.md"
    daily_content = f"""# {today}

## 今日主线

- 

## 今日任务池

- [ ] 

## 临时记录

- 

## 晚间回流

- 完成：
- 未完成且仍重要：
- 应写回项目：
- 可沉淀方法：
"""
    results.append(f"{write_if_missing(daily, daily_content, args.force)}: {daily.relative_to(root)}")

    project_root = root / "30_Projects" / args.project
    for rel, content in PROJECT_FILES.items():
        result = write_if_missing(project_root / rel, content, args.force)
        results.append(f"{result}: {project_root.relative_to(root) / rel}")

    print(f"AI Personal Work OS initialized at: {root}")
    print("\n".join(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

