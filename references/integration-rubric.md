# Integration Rubric

## Decision Tiers

- **Adopt**: grounded in provided material, actionable, safe, and aligned with the user's goal.
- **Consider**: useful direction, but needs verification, user choice, or local adaptation.
- **Flag**: possible issue or conflict that should be surfaced, not silently resolved.
- **Reject**: hallucinated, unsupported, unsafe, private-data-seeking, off scope, too broad, or violates user style constraints.

## Comparison Matrix

```markdown
| Provider | Model/Mode | Suggestion | Evidence in Packet | Risk | Fit to User Goal | Decision | Reason | Action |
|---|---|---|---|---|---|---|---|---|
| Claude | Sonnet |  | high/medium/low | high/medium/low | high/medium/low | Adopt/Consider/Flag/Reject |  |  |
```

## Synthesis Rules

1. Do not treat majority agreement as truth.
2. Prefer verified local files and official sources over external AI claims.
3. Separate style advice from factual claims.
4. Do not adopt new facts, numbers, citations, API behavior, prices, policies, or legal/medical/financial guidance without verification.
5. Reject broad rewrites when the user requested a narrow fix.
6. Preserve the user's explicit style constraints, even if an external AI suggests a polished but disallowed phrase.
7. Explain major rejections briefly; the user should see the boundary logic.

## Common Rejection Reasons

- Invented or unsupported data.
- Requests to upload private material.
- Conflicts with local project facts.
- Violates the user's wording restrictions.
- Adds scope, features, experiments, or refactors not requested.
- Too generic to act on.
- Risk exceeds benefit.

## Final Absorption Record

Use this structure:

```markdown
# External AI Absorption Record

## Providers Used
| Provider | Model/Mode | Status | Notes |
|---|---|---|---|

## Adopted
| Suggestion | Source | Why Adopted | Where Applied |
|---|---|---|---|

## Partially Used
| Suggestion | Source | What Was Kept | What Was Dropped |
|---|---|---|---|

## Rejected
| Suggestion | Source | Reason |
|---|---|---|

## Still Needs Verification
| Claim or Action | Verification Source Needed |
|---|---|
```
