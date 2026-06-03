---
name: ai-personal-work-os
description: Use when a user wants to build, initialize, operate, or refactor a personal AI work system for Obsidian or local Markdown files, especially when they want agents to manage projects, Daily notes, action pools, next actions, decision logs, and reusable workflows rather than just create static templates.
metadata:
  short-description: Build and run a personal AI work OS
---

# AI Personal Work OS

This skill turns a local folder or Obsidian vault into a running AI work system.

Important: initializing the folder structure is only the first step. The system becomes useful only after the agent helps the user map real projects, daily actions, write-back rules, and decision boundaries into the structure.

Use it when the user asks to:

- create a personal AI work system
- set up an Obsidian/Codex/Agent project workflow
- generate project folders, Daily notes, action pools, or agent rules
- make AI remember project context across sessions
- turn scattered work into a repeatable AI enablement system

## Core Model

The system is not a set of isolated files. It is a flow:

```text
Inbox / voice / ideas
  -> Action Pool
  -> Today Daily
  -> Project _next.md
  -> Work execution
  -> State / decision write-back
  -> Reusable methods
```

Every project has five operating files:

- `_项目规则.md`: project boundaries, read paths, write-back rules
- `_总览.md`: durable context and positioning
- `_当前状态.md`: current state and confirmed facts
- `_next.md`: the single active next action
- `决策日志.md`: major decisions and irreversible tradeoffs

## Default Procedure

1. Ask for or infer a target root folder.
2. If creating a new system, run `scripts/init_work_os.py --root <target>`.
3. If adapting an existing vault, inspect only top-level structure and relevant project files.
4. Create or update the operating files without moving unrelated user files.
5. Identify one real project or daily workflow to connect first.
6. Explain the operating flow and the next daily/project action.

## Operating Rules for Agents

When entering a workspace:

1. Read `_索引.md` first.
2. If working inside a project, read that project’s `_项目规则.md`.
3. Read `_next.md` before doing work.
4. Do only the current action unless the user explicitly expands scope.
5. After completion:
   - write the result and next action to `_next.md`
   - update `_当前状态.md` if project state changed
   - update `决策日志.md` only for major decisions
   - put cross-project actions back into `40_Daily/_行动池.md`

## Daily Flow

Use this flow when the user asks for daily planning, task capture, or review:

1. Capture loose inputs in `00_Inbox/` or directly in `40_Daily/_行动池.md`.
2. During planning, pull only today-sized actions into `40_Daily/days/YYYY/YYYY-MM-DD.md`.
3. For project work, Daily links to the project `_next.md`; it does not duplicate full project context.
4. At day end:
   - completed actions stay in Daily
   - unfinished project actions return to project `_next.md`
   - cross-project or future items return to `_行动池.md`
   - reusable patterns go to `20_Insights/`

Do not overbuild Daily. Daily should only hold today’s execution focus; durable context belongs in projects.

## Project Flow

Use this flow when creating or continuing a project:

1. Create the project folder under `30_Projects/<area>/<project>` or `30_Projects/<project>`.
2. Add the five operating files.
3. Put only one active action at the top of `_next.md`.
4. Keep source materials and large outputs outside the vault; store only references and decisions.
5. When work completes, archive the action at the bottom of `_next.md`, then write the new single next action.

Projects should produce actions, but not every project note belongs in Daily. Daily pulls only the actions that are executable today.

## Safety

Never write secrets, tokens, passwords, private keys, server IPs, customer private data, or full login commands into the workspace.

Use placeholders such as:

- `YOUR_EXTERNAL_WORKSPACE`
- `YOUR_SECRET_STORE`
- `YOUR_SERVER_ALIAS`
- `YOUR_API_KEY_ENV_NAME`

For more detail, read `references/operating-flow.md` when the user asks how the system moves, and use `scripts/init_work_os.py` when generating the folder structure.
