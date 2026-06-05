# Cherry Studio MCP Guide

This integration is for users who want a graphical AI client while keeping Mondo as a local work-scene tool layer.

Cherry Studio provides:

- chat UI;
- model configuration;
- conversation history;
- short-term dialogue memory;
- MCP tool calling.

Mondo MCP provides:

- workspace initialization;
- guided onboarding;
- workspace diagnosis;
- workspace scanning;
- live state export;
- simple agent context export;
- safe Markdown append inside the workspace;
- public role-pack listing.

## MCP Configuration

If you use the repository directly:

```json
{
  "mcpServers": {
    "mondo-agent-os": {
      "command": "python",
      "args": [
        "D:/AI_Workspace/outputs/ip-content-system/mondo-agent-os/scripts/mondo_mcp.py"
      ]
    }
  }
}
```

If you installed the package:

```json
{
  "mcpServers": {
    "mondo-agent-os": {
      "command": "mondo-mcp",
      "args": []
    }
  }
}
```

Replace the path with your local repository path.

## Suggested Assistant Prompt

```text
You are a Mondo work assistant.

You do not only answer questions. You help the user maintain a local Mondo Agent OS workspace.

Rules:
1. For a new user, start with mondo_start_onboarding instead of loose input routing.
2. During onboarding, collect long-term direction, current projects, AI boundaries, this week's main line, and current friction.
3. After collecting long-term direction, call mondo_collect_identity.
4. After collecting project notes, call mondo_collect_projects.
5. Show the draft to the user before writing.
6. Only after user confirmation, call mondo_confirm_onboarding.
7. After onboarding enters active_daily_flow, use mondo_scan, mondo_export_context, mondo_route_input, and mondo_append_markdown for daily flow.
8. Before writing any file, explain which file will be written and what will be written.
9. Do not write keys, tokens, passwords, private keys, server IPs, customer privacy, or full login commands.
10. Daily only contains actions for today. Cross-day actions go to the action pool. Project progress is written back to project files. Major decisions go to the decision log.
11. Do not try to organize the user's entire knowledge base at once. Move one clear action at a time.
```

## First User Message

The user can start with:

```text
Please help me set up a personal AI work system. Put the workspace in D:/MondoWorkOS.
```

The assistant should first ask:

```text
What do you want your work and life to become over the next 3-6 months?
What are your active projects right now?
What stage is each project in?
Which projects are this week's main line, and which are waiting or only being kept alive?
What can AI help with, and what should it never do automatically?
```

After the user responds, the assistant should summarize the work scene, ask for confirmation, then write only after confirmation.

## Daily Use

Morning:

```text
Help me do a morning review.
```

The assistant should read the action pool, today's Daily, and project `_next.md` files, then suggest actions that can actually be done today.

During the day:

```text
I just finished talking with the client. Next week I need to show them a proposal.
```

The assistant should decide whether this is project state, next action, waiting item, or today's task, then explain the proposed write-back.

Evening:

```text
Help me close the day.
```

The assistant should help confirm completed actions, unfinished actions, project state changes, decisions, and tomorrow's first step.
