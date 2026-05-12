# AI Group Review Workflow

## Phase 0: Intake

Confirm these points before preparing any external prompt:

- Review goal: what decision or deliverable the user wants.
- Target providers: Claude, ChatGPT, DeepSeek, Gemini, Grok, or others.
- Output format: findings, rewrite, comparison table, plan, code review, prompt, script, or memory aid.
- Source material: exact files, excerpts, drafts, screenshots, logs, or summaries.
- Boundaries: what must not be sent, uploaded, changed, or invented.
- Verification needs: which claims must be checked against local files or official sources.

If the user only gives a broad request, ask a short clarification before contacting external AI.

## Phase 1: Build the Prompt Packet

Use a packet instead of a short question. A useful packet normally includes:

- Review goal.
- Project or task background.
- Current draft, excerpt, code snippet, plan, or slide text.
- Known facts and assumptions, clearly separated.
- User constraints and style restrictions.
- What to review.
- What not to do.
- Required output format.
- Privacy notice telling the external AI not to request private identifiers, account data, full files, or unapproved uploads.

Prefer excerpts and summaries. Only include the minimum context needed for a high-quality review.

## Phase 2: Sanitize and Scan

Before sending:

1. Replace personal names, organizations, clients, schools, local paths, unpublished titles, and private identifiers with stable placeholders.
2. Remove secrets, tokens, credentials, cookies, private URLs, internal IDs, and unrelated metadata.
3. Run `scripts/scan_prompt_risks.py`.
4. If high-risk content remains, stop and ask the user how to proceed.
5. If upload is proposed, create an upload manifest with file, destination, purpose, risk, and confirmation status.

The scanner is a first pass, not a guarantee. Human review is still required.

## Phase 3: Approval Gate

Show the exact outbound text when the prompt includes sensitive project context or when the user asks to approve before sending.

For file upload, require explicit approval naming the files and destination AI. Do not infer approval from general consent to use external AI.

## Phase 4: External AI Execution

For each provider:

1. Verify the site is logged in.
2. Verify the requested model or mode is selected, when visible.
3. Send the approved prompt or approved chunk.
4. If the prompt is split, send all read-only chunks first, then a final review instruction.
5. Wait for completion.
6. If the response is truncated, request continuation once if appropriate.
7. Save the raw response and metadata before integrating.

Record blockers such as login failure, CAPTCHA, model unavailable, rate limit, empty response, network error, or manual refresh required. Do not use another provider or model as a silent substitute.

## Phase 5: Archive

Each run should have a stable local folder, for example:

```text
ai-group-review-runs/
  20260512-1530-task-slug/
    manifest.json
    00-request.md
    01-prompt-packets/
      round1.md
      round1-sanitized.md
    02-external-ai/
      claude/round1-raw.md
      chatgpt/round1-raw.md
      deepseek/round1-blocker.md
    03-synthesis/
      comparison-matrix.md
      accepted-rejected.md
    04-validation.md
```

Raw external responses stay local unless the user explicitly asks to publish them.

## Phase 6: Synthesis

Use the integration rubric:

- Adopt: useful, grounded, safe, and aligned with the user request.
- Consider: plausible but needs human judgment or source verification.
- Flag: risk, conflict, or missing evidence.
- Reject: hallucinated, unsafe, unsupported, private-data-seeking, off scope, or style-violating.

External AI consensus is not proof. A minority suggestion can be adopted if it is better supported by local facts.

## Phase 7: Follow-up Rounds

Use a second round when the first round reveals missing templates, failure modes, or concrete implementation questions. The second prompt should include a short synthesis of accepted first-round themes, not the full raw replies unless needed and safe.
