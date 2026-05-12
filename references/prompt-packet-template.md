# Prompt Packet Templates

## Master Packet

```text
# Review Goal
[What the user wants reviewed and what decision or deliverable is needed.]

# Context
[Necessary project/task background. Keep it rich enough for judgment but sanitized.]

# Material to Review
[Excerpt, draft, code snippet, plan, slide text, or summarized file contents.]

# Known Facts
- Verified:
- Inferred:
- Unknown / needs verification:

# User Constraints
- Must keep:
- Must avoid:
- Do not change:
- Style preferences:

# Review Questions
1.
2.
3.

# What Not to Do
- Do not invent facts, numbers, sources, citations, experiments, prices, schedules, or model capabilities.
- Do not request private files, names, paths, accounts, secrets, or identifiers.
- Do not expand scope beyond the stated task.

# Expected Output
[Findings table, rewrite, plan, comparison, code review, prompt, Q&A, etc.]

# Privacy Notice
This packet is sanitized. Do not ask for real names, full private files, account details, credentials, local paths, or unapproved uploads.
```

## Round 1 Review Prompt

```text
You are one of several external reviewers. Review the material below under the stated constraints.

Focus on:
1. Problems or risks.
2. Concrete improvements.
3. Missing context that would change the recommendation.
4. Items that should not be changed.

Return:
## Critical Issues
## Suggested Improvements
## Useful Examples or Alternatives
## Keep / Reject
## Concise Recommended Next Step
```

## Round 2 Delta Prompt

```text
Several reviewers converged on these themes:
[Short synthesis. Do not paste private raw replies unless safe and necessary.]

Now provide concrete implementation advice for:
- file contents,
- templates,
- failure modes,
- validation,
- examples,
- what to exclude.

Keep the advice generic and safe for public use.
```

## File Upload Approval Request

```text
I propose uploading these files to [AI provider/model]:

| File | Purpose | Sensitive Content Risk | Why an excerpt is not enough | Destination | Approval |
|---|---|---|---|---|---|
| [name] | [reason] | [low/medium/high] | [reason] | [provider] | pending |

Risks:
- Third-party AI services may store or process uploaded content under their own policies.
- Uploaded files may expose names, paths, unpublished material, customer data, or internal structure.

Please explicitly confirm whether to upload these exact files, or ask me to prepare sanitized excerpts instead.
```

## Chunk Header

Use this when a prompt exceeds the web UI limit.

```text
Part [N]/[TOTAL]. Read and acknowledge only. Do not review yet.

[chunk content]
```

Final chunk:

```text
Part [N]/[TOTAL]. This is the final part. Now review all parts together using the requested output format.
```
