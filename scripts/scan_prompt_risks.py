#!/usr/bin/env python3
"""Scan an outbound external-AI prompt for common privacy and secret risks."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}


@dataclass
class Finding:
    severity: str
    kind: str
    line: int
    snippet: str


PATTERNS: list[tuple[str, str, str]] = [
    ("high", "openai_or_similar_key", r"\bsk-[A-Za-z0-9_\-]{20,}\b"),
    ("high", "github_token", r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{20,}\b"),
    ("high", "google_api_key", r"\bAIza[0-9A-Za-z_\-]{20,}\b"),
    ("high", "slack_token", r"\bxox[baprs]-[A-Za-z0-9\-]{20,}\b"),
    ("high", "jwt_like_token", r"\beyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b"),
    ("high", "private_key_header", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("medium", "windows_absolute_path", r"\b[A-Za-z]:\\[^\s<>:\"|?*]+"),
    ("medium", "unc_path", r"\\\\[A-Za-z0-9_.\-]+\\[^\s<>:\"|?*]+"),
    ("medium", "unix_home_path", r"/home/[A-Za-z0-9_.\-]+/[^\s]+|/Users/[A-Za-z0-9_.\-]+/[^\s]+"),
    ("medium", "email", r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    ("medium", "phone_like", r"(?<!\d)(?:\+?\d{1,3}[- ]?)?(?:\d[- ]?){10,14}(?!\d)"),
    ("medium", "secret_marker", r"(?i)\b(password|passwd|secret|token|api[_-]?key|credential|cookie)\b|密码|密钥|令牌|凭证"),
    ("medium", "personal_marker", r"身份证|手机号|家庭住址|银行卡|护照|学生证|工号"),
    ("low", "doi", r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b"),
]


def scan(text: str, allow_paths: bool, allow_doi: bool) -> list[Finding]:
    findings: list[Finding] = []
    enabled = []
    for severity, kind, pattern in PATTERNS:
        if allow_paths and kind in {"windows_absolute_path", "unc_path", "unix_home_path"}:
            continue
        if allow_doi and kind == "doi":
            continue
        enabled.append((severity, kind, re.compile(pattern)))

    for line_no, line in enumerate(text.splitlines(), start=1):
        for severity, kind, regex in enabled:
            for match in regex.finditer(line):
                snippet = match.group(0)
                if len(snippet) > 120:
                    snippet = snippet[:117] + "..."
                findings.append(Finding(severity, kind, line_no, snippet))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Prompt packet file to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.add_argument("--fail-on", choices=["low", "medium", "high"], default="high", help="Exit 2 when this severity or above is found.")
    parser.add_argument("--allow-paths", action="store_true", help="Do not flag absolute filesystem paths.")
    parser.add_argument("--allow-doi", action="store_true", help="Do not flag DOI strings.")
    args = parser.parse_args()

    path = Path(args.input).expanduser().resolve()
    text = path.read_text(encoding="utf-8")
    findings = scan(text, allow_paths=args.allow_paths, allow_doi=args.allow_doi)

    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    else:
        if not findings:
            print("No risk patterns found.")
        for finding in findings:
            print(f"{finding.severity.upper()} line {finding.line} {finding.kind}: {finding.snippet}")
        if findings:
            print("\nNote: this scanner is a first pass only. Review outbound content manually before sending.")

    threshold = SEVERITY_RANK[args.fail_on]
    if any(SEVERITY_RANK[f.severity] >= threshold for f in findings):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
