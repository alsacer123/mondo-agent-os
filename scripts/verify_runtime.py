#!/usr/bin/env python3
"""Smoke-test the Mondo Agent OS runtime."""

from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mondo_agent_os.cli import main as cli_main  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "work-os"

        cli_main(["init", "--root", str(workspace), "--project", "测试项目"])

        doctor_out = io.StringIO()
        with contextlib.redirect_stdout(doctor_out):
            doctor_code = cli_main(["doctor", "--root", str(workspace), "--json"])
        if doctor_code != 0:
            print(doctor_out.getvalue())
            return doctor_code
        report = json.loads(doctor_out.getvalue())
        assert report["status"] == "ok", report
        assert report["projects_checked"] == 1, report

        scan_out = io.StringIO()
        with contextlib.redirect_stdout(scan_out):
            cli_main(["scan", "--root", str(workspace)])
        system_map = json.loads(scan_out.getvalue())
        assert system_map["projects"][0]["path"] == "30_Projects\\测试项目" or system_map["projects"][0]["path"] == "30_Projects/测试项目"

        route_out = io.StringIO()
        with contextlib.redirect_stdout(route_out):
            cli_main(["route", "今天把客户项目的下一步写回"])
        routed = json.loads(route_out.getvalue())
        assert routed["target"] == "daily", routed

        packs_out = io.StringIO()
        with contextlib.redirect_stdout(packs_out):
            cli_main(["packs", "--json"])
        role_packs = json.loads(packs_out.getvalue())
        assert "content-personal-brand" in role_packs

        live_out = io.StringIO()
        with contextlib.redirect_stdout(live_out):
            cli_main(["live", "--root", str(workspace)])
        assert (workspace / ".mondo" / "live-state.json").exists()

        context_out = io.StringIO()
        with contextlib.redirect_stdout(context_out):
            cli_main(["context", "--root", str(workspace)])
        context_file = workspace / ".mondo" / "agent-context.md"
        assert context_file.exists()
        assert "Mondo Agent Context" in context_file.read_text(encoding="utf-8")

        beta_pack_out = io.StringIO()
        beta_pack_file = Path(tmp) / "first-beta-run-pack.md"
        with contextlib.redirect_stdout(beta_pack_out):
            cli_main(["beta-pack", "--output", str(beta_pack_file)])
        assert beta_pack_file.exists()
        assert "First Beta Run Pack" in beta_pack_file.read_text(encoding="utf-8")

        beta_intake_out = io.StringIO()
        beta_intake_file = Path(tmp) / "beta-user-intake.md"
        with contextlib.redirect_stdout(beta_intake_out):
            cli_main(["beta-intake", "--output", str(beta_intake_file)])
        assert beta_intake_file.exists()
        assert "第一位内测候选用户准入记录" in beta_intake_file.read_text(encoding="utf-8")

        beta_outreach_out = io.StringIO()
        beta_outreach_file = Path(tmp) / "beta-candidate-outreach.md"
        with contextlib.redirect_stdout(beta_outreach_out):
            cli_main(["beta-outreach", "--output", str(beta_outreach_file)])
        assert beta_outreach_file.exists()
        assert "第一位内测候选触达清单" in beta_outreach_file.read_text(encoding="utf-8")

        beta_status_out = io.StringIO()
        with contextlib.redirect_stdout(beta_status_out):
            cli_main(["beta-status", "--root", str(ROOT), "--json"])
        beta_status = json.loads(beta_status_out.getvalue())
        assert beta_status["status"] in {"missing_artifacts", "ready_for_candidate_outreach"}
        assert len(beta_status["artifacts"]) == 3

        from mondo_agent_os.workspace import append_markdown

        append_markdown(
            workspace,
            "40_Daily/_行动池.md",
            "- [ ] 整理第一个内测用户反馈",
            "内测输入",
        )
        assert "内测输入" in (workspace / "40_Daily" / "_行动池.md").read_text(encoding="utf-8")

    print("runtime smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
