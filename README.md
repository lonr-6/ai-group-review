# ai-group-review

`ai-group-review` is a Codex skill for coordinating privacy-conscious reviews with browser-based external AI systems.

It helps an assistant prepare rich but sanitized prompt packets, send them to tools such as Claude, ChatGPT, DeepSeek, Gemini, Grok, or similar web AI products, archive the replies locally, and synthesize useful suggestions without blindly following external model output.

This is a Codex skill, not a standalone web service, API wrapper, browser extension, or model gateway. It does not require API keys.

## When to Use It

Use this skill when a task would benefit from outside AI review, for example:

- reviewing academic writing, proposals, literature reviews, or presentation scripts;
- asking several models to critique a plan, prompt, or product memo;
- comparing external AI feedback on a code change or architecture decision;
- saving external AI replies locally so the review trail is not lost in browser context;
- integrating several model opinions while keeping local project facts and user constraints in control.

## Core Idea

External AI systems are treated as advisors, not authorities.

The assistant should:

1. clarify the review goal and boundaries;
2. build a complete but sanitized prompt packet;
3. run a local risk scan before sending;
4. use only the requested browser AI tools;
5. record actual provider, model or mode, prompt version, status, and blockers;
6. archive every external response locally;
7. classify suggestions as `Adopt`, `Consider`, `Flag`, or `Reject`;
8. produce an integrated answer grounded in local facts and the user's stated constraints.

## Repository Layout

```text
ai-group-review/
  SKILL.md
  agents/openai.yaml
  references/
    workflow.md
    prompt-packet-template.md
    privacy-and-boundaries.md
    cases.md
    integration-rubric.md
    external-ai-platforms.md
  scripts/
    create_review_workspace.py
    split_prompt_packet.py
    scan_prompt_risks.py
```

## What Each File Does

- `SKILL.md` defines when the skill should be used and the core operating rules.
- `references/workflow.md` gives the full review workflow from intake to synthesis.
- `references/prompt-packet-template.md` provides reusable prompt packet templates.
- `references/privacy-and-boundaries.md` defines sanitization, file-upload, and stop rules.
- `references/cases.md` contains sanitized examples for academic writing, code review, product review, and presentation scripts.
- `references/integration-rubric.md` explains how to compare, adopt, flag, or reject external AI suggestions.
- `references/external-ai-platforms.md` gives practical notes for browser-based AI tools and manual fallback.
- `agents/openai.yaml` provides UI-facing metadata for Codex skill lists.

## Helper Scripts

The scripts use only the Python standard library.

Create a local review workspace:

```bash
python scripts/create_review_workspace.py --root ./ai-group-review-runs --task thesis-section-review --providers claude,chatgpt,gemini --rounds 1
```

Split a long prompt packet into browser-friendly chunks:

```bash
python scripts/split_prompt_packet.py prompt.md --max-chars 8000 --out-dir ./prompt-parts
```

Scan an outbound prompt for common privacy and secret risks:

```bash
python scripts/scan_prompt_risks.py prompt.md
```

The risk scanner is a first pass only. It can flag common patterns such as secrets, absolute paths, emails, phone-like strings, and sensitive markers, but it does not replace human review.

## Example Use

A user asks:

```text
Use Claude, Gemini, and ChatGPT to review this sanitized presentation script.
Check for unclear logic, overly generic phrasing, unsupported claims, and likely audience questions.
Save each model's reply locally and give me an integrated version.
```

The skill guides the assistant to:

- confirm the review goal and off-limits material;
- prepare a complete prompt packet;
- scan and sanitize the outbound content;
- ask for approval if sensitive material or file upload is involved;
- query the requested web AI tools;
- archive their replies;
- synthesize the final answer with a clear adoption and rejection record.

## Privacy Boundaries

By default, do not upload files. Prefer sanitized excerpts and summaries.

Never send:

- API keys, tokens, credentials, cookies, private keys, or session data;
- `.env` files, database URLs, private deployment configs, or internal secrets;
- raw personal data, student records, medical data, financial records, or account screenshots;
- full proprietary documents, unpublished manuscripts, customer contracts, or raw datasets without explicit approval;
- local path mappings or private identifiers that are not necessary for the review.

If file upload is useful, the assistant should first create an upload manifest that lists the exact files, destination AI, purpose, risk, and confirmation status.

## Handling External AI Output

External AI output should be filtered, not copied directly.

Reject suggestions that:

- invent facts, citations, numbers, versions, prices, or capabilities;
- request private files or account details;
- conflict with local project facts;
- violate the user's style or scope constraints;
- recommend broad rewrites when the user asked for a narrow fix;
- override the skill's privacy or safety boundaries.

## Notes

- Browser AI websites change often. The skill therefore describes a stable workflow instead of relying on fragile website selectors.
- Partial reviews are acceptable when missing providers are logged as blockers.
- Local archives may still contain sensitive review context. Keep them out of public repositories unless they are intentionally sanitized.
