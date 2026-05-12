#!/usr/bin/env python3
"""Create a local archive workspace for an external AI group review."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


DEFAULT_PROVIDERS = "claude,chatgpt,deepseek,gemini,grok"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "review"


def write_if_missing(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"DRY-RUN create {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Parent directory for review workspaces.")
    parser.add_argument("--task", default="review", help="Short task name used in the folder slug.")
    parser.add_argument("--providers", default=DEFAULT_PROVIDERS, help="Comma-separated provider list.")
    parser.add_argument("--rounds", type=int, default=2, help="Number of planned review rounds.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned files without writing.")
    args = parser.parse_args()

    providers = [p.strip().lower() for p in args.providers.split(",") if p.strip()]
    if not providers:
        raise SystemExit("No providers specified.")
    if args.rounds < 1:
        raise SystemExit("--rounds must be at least 1.")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    workspace = Path(args.root).expanduser().resolve() / f"{timestamp}-{slugify(args.task)}"

    manifest = {
        "task": args.task,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "providers": providers,
        "rounds": args.rounds,
        "status": "prepared",
    }

    write_if_missing(workspace / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", args.dry_run)
    write_if_missing(workspace / "00-request.md", "# Request\n\n- Goal:\n- Target providers:\n- Output expected:\n- Off-limits material:\n", args.dry_run)

    for round_no in range(1, args.rounds + 1):
        write_if_missing(workspace / "01-prompt-packets" / f"round{round_no}.md", f"# Round {round_no} Prompt Packet\n\n", args.dry_run)
        write_if_missing(workspace / "01-prompt-packets" / f"round{round_no}-sanitized.md", f"# Round {round_no} Sanitized Prompt Packet\n\n", args.dry_run)
        for provider in providers:
            write_if_missing(workspace / "02-external-ai" / provider / f"round{round_no}-raw.md", f"# {provider} round {round_no} raw response\n\n", args.dry_run)
            write_if_missing(workspace / "02-external-ai" / provider / f"round{round_no}-metadata.json", "{}\n", args.dry_run)

    write_if_missing(workspace / "03-synthesis" / "comparison-matrix.md", "# Comparison Matrix\n\n| Provider | Model/Mode | Suggestion | Evidence | Risk | Fit | Decision | Reason | Action |\n|---|---|---|---|---|---|---|---|---|\n", args.dry_run)
    write_if_missing(workspace / "03-synthesis" / "accepted-rejected.md", "# Accepted and Rejected Suggestions\n\n", args.dry_run)
    write_if_missing(workspace / "04-validation.md", "# Validation\n\n- Risk scan:\n- External responses archived:\n- Facts verified:\n- Remaining manual checks:\n", args.dry_run)

    print(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
