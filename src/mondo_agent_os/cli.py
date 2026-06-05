"""Command line interface for Mondo Agent OS."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from .beta_pack import write_first_beta_pack
from .spec import ROLE_PACKS
from .workspace import (
    doctor_workspace,
    export_agent_context,
    init_workspace,
    route_input,
    scan_workspace,
    to_json,
    write_live_state,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mondo-os")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Initialize a Mondo Agent OS workspace")
    init.add_argument("--root", required=True)
    init.add_argument("--project", default="示例AI赋能项目")
    init.add_argument("--force", action="store_true")

    doctor = sub.add_parser("doctor", help="Check whether a workspace is operable")
    doctor.add_argument("--root", required=True)
    doctor.add_argument("--json", action="store_true")

    scan = sub.add_parser("scan", help="Print a workspace map")
    scan.add_argument("--root", required=True)

    route = sub.add_parser("route", help="Route one loose input to the right OS layer")
    route.add_argument("text")

    packs = sub.add_parser("packs", help="List available role packs")
    packs.add_argument("--json", action="store_true")

    live = sub.add_parser("live", help="Write live state for agents or simple dashboards")
    live.add_argument("--root", required=True)
    live.add_argument("--watch", action="store_true", help="Keep refreshing live state")
    live.add_argument("--interval", type=int, default=60)

    context = sub.add_parser("context", help="Export a simple context file for non-Codex agents")
    context.add_argument("--root", required=True)

    beta_pack = sub.add_parser("beta-pack", help="Prepare a local first beta run pack")
    beta_pack.add_argument("--output", default=".mondo/first-beta-run-pack.md")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        root = Path(args.root)
        results = init_workspace(root, args.project, args.force)
        print(f"Mondo Agent OS initialized at: {root.expanduser().resolve()}")
        print("\n".join(results))
        return 0

    if args.command == "doctor":
        report = doctor_workspace(Path(args.root))
        if args.json:
            print(to_json(report))
        else:
            print(f"status: {report.status}")
            print(f"root: {report.root}")
            print(f"projects_checked: {report.projects_checked}")
            if report.missing_root_files:
                print("missing_root_files:")
                for item in report.missing_root_files:
                    print(f"- {item}")
            if report.projects_with_missing_files:
                print("projects_with_missing_files:")
                for item in report.projects_with_missing_files:
                    print(f"- {item.path}: {', '.join(item.missing_files)}")
            if report.secret_warnings:
                print("secret_warnings:")
                for item in report.secret_warnings:
                    print(f"- {item}")
        return 0 if report.status == "ok" else 1

    if args.command == "scan":
        print(to_json(scan_workspace(Path(args.root))))
        return 0

    if args.command == "route":
        print(to_json(route_input(args.text)))
        return 0

    if args.command == "packs":
        if args.json:
            print(to_json(ROLE_PACKS))
        else:
            for key, pack in ROLE_PACKS.items():
                print(f"{key}: {pack['name']} - {pack['description']}")
        return 0

    if args.command == "live":
        root = Path(args.root)
        if args.watch:
            while True:
                output = write_live_state(root)
                print(f"live state updated: {output}")
                time.sleep(max(args.interval, 5))
        output = write_live_state(root)
        print(f"live state updated: {output}")
        return 0

    if args.command == "context":
        output = export_agent_context(Path(args.root))
        print(f"agent context exported: {output}")
        return 0

    if args.command == "beta-pack":
        output = write_first_beta_pack(Path(args.output))
        print(f"first beta run pack written: {output}")
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
