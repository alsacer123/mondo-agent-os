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
            assert "mondo_append_markdown" in tool_names

            created = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_init_workspace",
                        "arguments": {"root": str(workspace), "project": "内测项目"},
                    },
                },
            )
            assert "results" in created["result"]["content"][0]["text"]

            context = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 4,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_export_context",
                        "arguments": {"root": str(workspace)},
                    },
                },
            )
            assert "agent-context.md" in context["result"]["content"][0]["text"]

            append = send(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 5,
                    "method": "tools/call",
                    "params": {
                        "name": "mondo_append_markdown",
                        "arguments": {
                            "root": str(workspace),
                            "relative_path": "40_Daily/_行动池.md",
                            "heading": "内测输入",
                            "content": "- [ ] 整理第一个内测用户反馈",
                        },
                    },
                },
            )
            assert "_行动池.md" in append["result"]["content"][0]["text"]
        finally:
            proc.kill()

    print("mcp smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
