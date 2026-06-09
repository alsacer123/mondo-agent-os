# Mondo Agent OS

Mondo Agent OS is a lightweight operating structure for personal AI work.

It is not a new chat client, a task app, or a complete agent runtime. Its goal is:

> Help people turn messy work into a work scene that AI can continuously understand, update, and help move forward.

The public repository contains the open base layer: workspace structure, operating rules, agent prompts, runtime checks, and optional helper tools. Business-specific role packs and consulting workflows should live outside the public base until they are mature enough to publish.

## Why It Exists

Most people do not fail with AI because they lack prompts. They fail because every conversation starts from zero:

- What is this project?
- What has already been decided?
- What can the AI read?
- What should not be touched?
- Where should results be written back?
- What is the next concrete step?

Mondo turns those answers into a stable local work scene.

## Customer Outcome

The desired user experience is:

1. First use: the user explains long-term direction and current projects in normal language.
2. After setup: the user sees projects, current state, next actions, Daily, and an action pool.
3. Morning: the system can connect yesterday's context with today's focus.
4. During the day: the user's agent can place loose inputs into the right layer.
5. Evening: completed work, project state changes, open loops, and tomorrow's first step can be closed.

## Current Layers

- Markdown OS: project rules, current state, one next step, decision log, Daily, and action pool.
- Agent Entry: Codex, Claude Code, Cherry Studio, Cursor, Cline, or another local-capable agent reads and writes the same workspace.
- Cherry Studio Assistant Setup: use Cherry Studio's model, memory, local file access, and tool calling to operate the Mondo workspace.
- Runtime Checks: optional CLI/MCP helpers for initialization, diagnosis, scanning, live state, and simple context export.
- Agent Skill: helps Codex/Claude-style agents create and maintain this structure.
- Role Packs: public examples of work-type protocols. Commercial or user-specific packs should remain separate.

## First Day

New users do not need to read every technical document first.

If you already use Codex, Claude Code, Obsidian, or Markdown workflows, start with the 10-minute skilled-user test:

- `docs/10-minute-skilled-user-test.md`

If you use Cherry Studio as the main agent client, start with:

- `docs/cherry-studio-agent-guide.md`

If you want the general non-technical first-day explanation, read:

- `docs/user-first-day-guide.md`

A user only needs:

- an AI client;
- an empty workspace folder;
- at least two real projects;
- a willingness to describe current work in normal language.

Example first message:

```text
Please help me set up a personal AI work system. Put the workspace in D:/MondoWorkOS.
```

The first-day goal is not to learn the file structure. The goal is to turn the user's long-term direction and current projects into a work scene that future AI sessions can keep reading.

## Quick Start

### CLI

```bash
pip install -e .
mondo-os init --root ./my-work-os --project "First AI-enabled project"
mondo-os doctor --root ./my-work-os
mondo-os scan --root ./my-work-os
mondo-os route "Today I need to write back the next step for the client project."
mondo-os packs
mondo-os live --root ./my-work-os
mondo-os context --root ./my-work-os
```

### Cherry Studio

Cherry Studio should be treated as an agent client, not as a thin MCP shell. Configure a Cherry Studio assistant with model access, memory, local file read/write ability, and the Mondo operating rules.

Start here:

- `docs/cherry-studio-agent-guide.md`

Optional Mondo MCP helper tools can still be configured for diagnosis, scan, live state, and context export.

Run the helper MCP server from the repository:

```bash
python scripts/mondo_mcp.py
```

Or after installation:

```bash
mondo-mcp
```

The helper MCP server is not the main workflow. The main workflow is: the assistant reads the Mondo OS files, understands the user's work, and writes back according to the OS rules.

### Manual Templates

You can also copy files from `templates/` into an Obsidian vault or normal folder:

1. Create `_索引.md` as the global entry.
2. Give each project a project rule file and runtime files.
3. Ask the AI to read `_项目规则.md` and `_next.md` before acting on a project.
4. After work is done, write results back to `_next.md`, `_当前状态.md`, or `决策日志.md`.

## Runtime Commands

```bash
mondo-os init --root <path> --project <name>
```

Initialize a minimal work system.

```bash
mondo-os doctor --root <path>
```

Check whether the workspace has the required structure and obvious secret leaks.

```bash
mondo-os scan --root <path>
```

Print a compact workspace map for agents or automation.

```bash
mondo-os route "one loose input"
```

Suggest where a loose input belongs: Daily, action pool, project, insights, or inbox.

```bash
mondo-os packs
```

List public role-pack manifests.

```bash
mondo-os live --root <path>
mondo-os live --root <path> --watch --interval 30
```

Write `.mondo/live-state.json` for lightweight dashboards, GUI clients, or agents.

```bash
mondo-os context --root <path>
```

Write `.mondo/agent-context.md`, a simple context entry for normal chat agents.

## What This Repository Does Not Do

- It does not store keys, tokens, passwords, private keys, server IPs, or full login commands.
- It does not put videos, images, PDFs, dependencies, caches, or large files into the workspace.
- It does not try to organize an entire knowledge base in one pass.
- It does not replace the user's judgment with a fully autonomous worker.
- It does not publish private consulting workflows or user-specific role packs.

## Methodology

- `docs/customer-outcome.md`
- `docs/10-minute-skilled-user-test.md`
- `docs/user-first-day-guide.md`
- `docs/execution-roadmap.md`
- `docs/github-task-guide.md`
- `docs/methodology.md`
- `docs/personal-ai-enablement.md`
- `docs/security.md`
- `docs/setup-guide.md`
- `docs/technical-architecture.md`
- `docs/cherry-studio-agent-guide.md`
- `docs/cherry-studio-mcp.md`

## Agent Skill

The `skill/` directory lets compatible agents initialize and maintain this structure:

- `skill/SKILL.md`
- `skill/references/operating-flow.md`
- `skill/scripts/init_work_os.py`

Example:

```bash
python skill/scripts/init_work_os.py --root ./my-work-os --project "First AI-enabled project"
```

## Development Verification

Run the full local verification suite:

```bash
python scripts/verify_all.py
```

It runs:

- documentation reference checks;
- runtime smoke test;
- MCP smoke test;
- onboarding flow verification.

Individual checks:

```bash
python scripts/verify_docs.py
python scripts/verify_runtime.py
python scripts/verify_mcp.py
python scripts/verify_onboarding_flow.py
```

## Contact

For real work-scene integration, describe:

- what AI currently fails to remember;
- what projects or workflows need continuity;
- how your Daily, action pool, project state, and documents are organized;
- what safety boundaries the AI must respect.

Use GitHub Issues with the public scenario template when possible.
