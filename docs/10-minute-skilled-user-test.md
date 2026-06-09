# 10-Minute Skilled User Test

This path is for Codex / Obsidian / Markdown users who already have a local-capable agent.

It is not the full ordinary-user onboarding path. It is a quick test to verify whether Mondo Agent OS can turn one real work description into a usable local Markdown work scene.

## Minute 1: Prepare A Workspace

Create an empty folder:

```text
D:/MondoWorkOS
```

## Minute 2-3: Initialize

From the Mondo Agent OS repository:

```bash
cd D:/AI_Tools/mondo-agent-os
pip install -e .
mondo-os init --root D:/MondoWorkOS --project "第一个真实项目"
mondo-os doctor --root D:/MondoWorkOS
```

If you see:

```text
status: ok
```

the workspace structure is ready.

## Minute 4-7: Tell The Agent Real Work

Use Codex, Cherry Studio, Claude Code, Cursor, Cline, or another agent with local file read/write ability.

Send this message:

```text
请读取 D:/MondoWorkOS 这个 Mondo 工作区。
先读 _索引.md 和 AGENTS.md。
如果进入具体项目，先读该项目 _项目规则.md 和 _next.md。

我接下来会说我的长期方向、当前项目、每个项目状态和下一步。
请先整理成草稿，写入前告诉我写到哪些文件。
```

Then describe real work, for example:

```text
我未来 3-6 个月想把个人 AI 工作方式变成可公开复用的系统。
现在有三个项目：个人品牌内容系统、AI 热点日报流程、Mondo 开源内测。
个人品牌卡在选题和周更节奏。
AI 热点日报需要固定栏目和精选标准。
Mondo 开源内测要验证第一批 Codex / Obsidian / Markdown 用户能不能跑起来。
AI 可以整理和草拟，但不要自动删除、移动、覆盖文件，也不要写隐私和密钥。
```

## Minute 8: Confirm Write-Back

The agent should show a write plan before writing, such as:

```text
_Identity/长期方向.md
30_Projects/<项目名>/_总览.md
30_Projects/<项目名>/_当前状态.md
30_Projects/<项目名>/_next.md
30_Projects/<项目名>/决策日志.md
40_Daily/_行动池.md
today's Daily
```

Only confirm after the file plan looks right.

## Minute 9: Morning Review

Say:

```text
帮我做今天早间整理。
```

The agent should read the action pool, today's Daily, and project `_next.md` files. It should only select actions that can actually be done today.

## Minute 10: Evening Closeout

Say:

```text
帮我晚间收口。
```

The agent should confirm:

- what was completed today;
- where unfinished actions return;
- which project states changed;
- tomorrow's first action.

## What Should Work

- CLI initialization.
- `doctor` / `scan`.
- Multi-project Markdown structure.
- Agent reading `_索引.md`, `AGENTS.md`, project `_项目规则.md`, and project `_next.md`.
- Agent writing long-term direction, project state, next actions, Daily, action pool, and decision log.
- `mondo-os context` as a compact handoff file for another AI tool.

## Known Limits

- This path assumes the user already knows how to use a local-capable agent.
- `mondo-os route` is only a lightweight helper. Complex Chinese project updates should be judged by the agent, not by the route helper alone.
- The current product still depends on the agent's local file read/write ability and judgment.
- There is not yet a one-command multi-project initializer for ordinary users.

## Product Judgment

Ready for Codex / Obsidian / Markdown skilled-user testing.

Not yet a one-click ordinary-user product.
