#!/usr/bin/env python3
"""Split a long prompt packet into numbered browser-friendly chunks."""

from __future__ import annotations

import argparse
import math
from pathlib import Path


def split_paragraphs(text: str, max_chars: int) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    current_len = 0

    paragraphs = text.split("\n\n")
    for para in paragraphs:
        block = para if para.endswith("\n") else para
        add_len = len(block) + (2 if current else 0)
        if current and current_len + add_len > max_chars:
            parts.append("\n\n".join(current).strip() + "\n")
            current = [block]
            current_len = len(block)
        elif len(block) > max_chars:
            if current:
                parts.append("\n\n".join(current).strip() + "\n")
                current = []
                current_len = 0
            for start in range(0, len(block), max_chars):
                parts.append(block[start : start + max_chars])
        else:
            current.append(block)
            current_len += add_len

    if current:
        parts.append("\n\n".join(current).strip() + "\n")
    return parts or [""]


def header(index: int, total: int, mode: str) -> str:
    if total == 1:
        return ""
    if mode == "ack" and index < total:
        return f"Part {index}/{total}. Read and acknowledge only. Do not review yet.\n\n"
    if index < total:
        return f"Part {index}/{total}. Read this context. Do not review until the final part.\n\n"
    return f"Part {index}/{total}. This is the final part. Now review all parts together using the requested output format.\n\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Prompt packet file.")
    parser.add_argument("--max-chars", type=int, default=8000, help="Maximum characters per chunk before headers.")
    parser.add_argument("--out-dir", default="prompt-parts", help="Directory for chunk files.")
    parser.add_argument("--mode", choices=["ack", "review"], default="ack", help="Header style for non-final parts.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned chunks without writing.")
    args = parser.parse_args()

    if args.max_chars < 500:
        raise SystemExit("--max-chars must be at least 500.")

    source = Path(args.input).expanduser().resolve()
    text = source.read_text(encoding="utf-8")
    chunks = split_paragraphs(text, args.max_chars)
    total = len(chunks)
    out_dir = Path(args.out_dir).expanduser().resolve()

    digits = max(2, int(math.log10(total)) + 1 if total else 2)
    for i, chunk in enumerate(chunks, start=1):
        out = header(i, total, args.mode) + chunk
        target = out_dir / f"part-{i:0{digits}d}-of-{total:0{digits}d}.md"
        if args.dry_run:
            print(f"DRY-RUN {target} chars={len(out)}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(out, encoding="utf-8")

    print(f"{total} chunk(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
