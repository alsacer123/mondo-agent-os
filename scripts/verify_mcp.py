#!/usr/bin/env python3
"""Smoke-test the dependency-free MCP stdio server."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def send(proc: subprocess.Popen[str], message: dict) -> dict:
    assert proc.stdin is not None
    assert proc.stdout is not None
    proc.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline()
    if not line:
        raise RuntimeError("MCP server did not respond")
    return json.loads(line)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "work-os"
        proc = subprocess.Popen(
            [sys.executable, "scripts/mondo_mcp.py"],
            cwd=ROOT,
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            init = send(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
            assert init["result"]["serverInfo"]["name"] == "mondo-agent-os"

            tools = send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
            tool_names = {tool["name"] for tool in tools["result"]["tools"]}
            assert "mondo_init_workspace" in tool_names
            assert "mondo_start_onboarding" in tool_names
            assert "mondo_confirm_onboarding" in tool_names
            assert "mondo_append_markdown" in tool_names
            assert "mondo_prepare_beta_pack" in tool_names
            assert "mondo_prepare_beta_intake" in tool_names

            started = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_start_onboarding",
                        "arguments": {"root": str(workspace)},
                    },
                },
            )
            assert "collecting_identity" in started["result"]["content"][0]["text"]

            identity = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_collect_identity",
                        "arguments": {
                            "root": str(workspace),
                            "notes": "我想用 AI 把个人工作变成可持续推进的系统，当前不想每次都重新解释背景。",
                        },
                    },
                },
            )
            assert "collecting_projects" in identity["result"]["content"][0]["text"]

            projects = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_collect_projects",
                        "arguments": {
                            "root": str(workspace),
                            "notes": "我现在有两个项目：个人品牌内容系统和客户交付。个人品牌要继续写下一篇长文，客户交付要下周给方案。",
                        },
                    },
                },
            )
            assert "draft_ready" in projects["result"]["content"][0]["text"]

            confirmed = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 6,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_confirm_onboarding",
                        "arguments": {"root": str(workspace)},
                    },
                },
            )
            assert "active_daily_flow" in confirmed["result"]["content"][0]["text"]
            assert (workspace / "_Identity" / "长期方向.md").exists()
            assert (workspace / "40_Daily" / "_行动池.md").exists()

            context = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 7,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_export_context",
                        "arguments": {"root": str(workspace)},
                    },
                },
            )
            assert "agent-context.md" in context["result"]["content"][0]["text"]

            beta_pack = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 8,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_prepare_beta_pack",
                        "arguments": {"output": str(Path(tmp) / "mcp-beta-pack.md")},
                    },
                },
            )
            assert "mcp-beta-pack.md" in beta_pack["result"]["content"][0]["text"]
            assert (Path(tmp) / "mcp-beta-pack.md").exists()

            beta_intake = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 9,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_prepare_beta_intake",
                        "arguments": {"output": str(Path(tmp) / "mcp-beta-intake.md")},
                    },
                },
            )
            assert "mcp-beta-intake.md" in beta_intake["result"]["content"][0]["text"]
            assert (Path(tmp) / "mcp-beta-intake.md").exists()
        finally:
            proc.kill()

    print("mcp smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
