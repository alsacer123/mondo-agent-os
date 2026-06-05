"""Dependency-free MCP stdio server for Mondo Agent OS."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .beta_pack import write_first_beta_pack
from .spec import ROLE_PACKS
from .onboarding import (
    collect_identity,
    collect_projects,
    confirm_onboarding,
    onboarding_status,
    start_onboarding,
)
from .workspace import (
    append_markdown,
    doctor_workspace,
    export_agent_context,
    init_workspace,
    route_input,
    scan_workspace,
    to_json,
    write_live_state,
)

PROTOCOL_VERSION = "2024-11-05"

TOOLS: list[dict[str, Any]] = [
    {
        "name": "mondo_init_workspace",
        "description": "Initialize a Mondo Agent OS workspace with Daily, action pool, and one project.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string"},
                "project": {"type": "string", "default": "示例AI赋能项目"},
                "force": {"type": "boolean", "default": False},
            },
            "required": ["root"],
        },
    },
    {
        "name": "mondo_start_onboarding",
        "description": "Start a guided onboarding flow before using Daily/project routing. This is the default first step for a new user.",
        "inputSchema": {
            "type": "object",
            "properties": {"root": {"type": "string"}},
            "required": ["root"],
        },
    },
    {
        "name": "mondo_collect_identity",
        "description": "Capture the user's long-term direction, positioning, friction, and AI boundaries during onboarding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["root", "notes"],
        },
    },
    {
        "name": "mondo_collect_projects",
        "description": "Capture the user's active, waiting, and paused projects during onboarding and produce a draft.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["root", "notes"],
        },
    },
    {
        "name": "mondo_onboarding_status",
        "description": "Return onboarding phase, next questions, and draft if available.",
        "inputSchema": {
            "type": "object",
            "properties": {"root": {"type": "string"}},
            "required": ["root"],
        },
    },
    {
        "name": "mondo_confirm_onboarding",
        "description": "After user review, write the initial identity, project, action pool, and Daily files.",
        "inputSchema": {
            "type": "object",
            "properties": {"root": {"type": "string"}},
            "required": ["root"],
        },
    },
    {
        "name": "mondo_doctor",
        "description": "Check whether a Mondo workspace is operable and whether it has obvious secret leaks.",
        "inputSchema": {
            "type": "object",
            "properties": {"root": {"type": "string"}},
            "required": ["root"],
        },
    },
    {
        "name": "mondo_scan",
        "description": "Return a compact workspace map for the current Mondo workspace.",
        "inputSchema": {
            "type": "object",
            "properties": {"root": {"type": "string"}},
            "required": ["root"],
        },
    },
    {
        "name": "mondo_route_input",
        "description": "Route one loose user input to Daily, action pool, project, insights, or inbox.",
        "inputSchema": {
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
    },
    {
        "name": "mondo_live_state",
        "description": "Write .mondo/live-state.json so a GUI client or agent can read current Daily/project state.",
        "inputSchema": {
            "type": "object",
            "properties": {"root": {"type": "string"}},
            "required": ["root"],
        },
    },
    {
        "name": "mondo_export_context",
        "description": "Write .mondo/agent-context.md for normal chat agents that need a simple context entry.",
        "inputSchema": {
            "type": "object",
            "properties": {"root": {"type": "string"}},
            "required": ["root"],
        },
    },
    {
        "name": "mondo_prepare_beta_pack",
        "description": "Write a local first beta run pack so a GUI client can host the first real user test without command line steps.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "output": {
                    "type": "string",
                    "default": ".mondo/first-beta-run-pack.md",
                }
            },
        },
    },
    {
        "name": "mondo_append_markdown",
        "description": "Append confirmed content to one Markdown file inside the workspace. Ask the user before using it.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "root": {"type": "string"},
                "relative_path": {"type": "string"},
                "content": {"type": "string"},
                "heading": {"type": "string"},
            },
            "required": ["root", "relative_path", "content"],
        },
    },
    {
        "name": "mondo_role_packs",
        "description": "List public role-pack manifests available in Mondo Core.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def text_result(value: object) -> dict[str, Any]:
    text = value if isinstance(value, str) else to_json(value)
    return {"content": [{"type": "text", "text": text}]}


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "mondo_init_workspace":
        result = init_workspace(
            Path(arguments["root"]),
            arguments.get("project") or "示例AI赋能项目",
            bool(arguments.get("force", False)),
        )
        return text_result({"results": result})
    if name == "mondo_start_onboarding":
        return text_result(start_onboarding(Path(arguments["root"])))
    if name == "mondo_collect_identity":
        return text_result(collect_identity(Path(arguments["root"]), arguments["notes"]))
    if name == "mondo_collect_projects":
        return text_result(collect_projects(Path(arguments["root"]), arguments["notes"]))
    if name == "mondo_onboarding_status":
        return text_result(onboarding_status(Path(arguments["root"])))
    if name == "mondo_confirm_onboarding":
        return text_result(confirm_onboarding(Path(arguments["root"])))
    if name == "mondo_doctor":
        return text_result(doctor_workspace(Path(arguments["root"])))
    if name == "mondo_scan":
        return text_result(scan_workspace(Path(arguments["root"])))
    if name == "mondo_route_input":
        return text_result(route_input(arguments["text"]))
    if name == "mondo_live_state":
        path = write_live_state(Path(arguments["root"]))
        return text_result({"path": str(path)})
    if name == "mondo_export_context":
        path = export_agent_context(Path(arguments["root"]))
        return text_result({"path": str(path)})
    if name == "mondo_prepare_beta_pack":
        output = arguments.get("output") or ".mondo/first-beta-run-pack.md"
        path = write_first_beta_pack(Path(output))
        return text_result({"path": str(path)})
    if name == "mondo_append_markdown":
        path = append_markdown(
            Path(arguments["root"]),
            arguments["relative_path"],
            arguments["content"],
            arguments.get("heading"),
        )
        return text_result({"path": str(path)})
    if name == "mondo_role_packs":
        return text_result(ROLE_PACKS)
    raise ValueError(f"Unknown tool: {name}")


def handle_request(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    request_id = message.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "mondo-agent-os", "version": "0.1.0"},
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = message.get("params") or {}
        try:
            result = call_tool(params["name"], params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32000, "message": str(exc)},
            }
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> int:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = handle_request(message)
        except Exception as exc:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": str(exc)},
            }
        if response is not None:
            sys.stdout.write(to_json(response).replace("\n", "") + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
