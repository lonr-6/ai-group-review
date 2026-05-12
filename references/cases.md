# Sanitized Case Examples

## Case 1: Academic Writing Review

Use for thesis proposals, literature reviews, introductions, discussion sections, and grant-style background sections.

### Prompt Focus

```text
Review this sanitized STEM academic section. The goal is to reduce AI-like wording, deepen the literature review, remove unsupported claims, and improve paragraph logic without inventing data or citations.

Constraints:
- Do not add unverified numbers, citations, journal names, or experimental conditions.
- Avoid stiff transitions such as "not X but Y" and "not in X but in Y".
- Avoid invented compound terms and slogan-like frameworks.
- Avoid hollow literature review statements such as "Author A demonstrated improvement" without conditions, data, or mechanism.
- Avoid unsupported claims such as "first", "leading", "fills a blank", or "complete proof".
- Preserve the author's technical scope.

Expected output:
1. Sentences that sound AI-like or too generic.
2. Unsupported claims that need evidence.
3. Logic jumps between paragraphs.
4. Conservative replacement text.
5. Items requiring the author to verify data or source material.
```

### Good External AI Suggestion

Identifies that "the figure supports the mechanism" is too vague and rewrites it into an actual result description: "The microscopy images show a thinner layered morphology after treatment, while the spectroscopy signal indicates increased defect-related sites."

### Reject

- Adds fabricated performance numbers.
- Invents citations.
- Rewrites the section into promotional language.
- Uses rigid contrast templates that the user explicitly banned.

## Case 2: Code Review

Use when the user wants outside review of a patch, error, API design, migration plan, or test strategy.

### Prompt Focus

```text
Review this sanitized code excerpt and change plan. Focus on correctness, security, edge cases, and missing tests. Do not suggest a broad rewrite unless it is necessary to fix the stated issue.

Constraints:
- No secrets, `.env`, private URLs, tokens, or production credentials are included.
- Do not ask for the full repository unless the missing context is essential.
- Separate confirmed bugs from speculative risks.
- Keep suggestions scoped to the user's requested change.
```

### Reject

- "Paste your database URL."
- "Disable validation to fix it."
- "Rewrite the whole auth system" when the task is a narrow UI bug.

## Case 3: Product or Strategy Review

Use for product plans, customer-facing proposals, workflow design, pricing narratives, or roadmap memos.

### Prompt Focus

```text
Review this sanitized strategy memo. Customer names, pricing, revenue, contracts, and private operating details have been removed.

Check:
- positioning clarity;
- user value;
- weak assumptions;
- execution sequence;
- risk and dependency gaps;
- wording that sounds generic or overconfident.

Treat market claims as hypotheses unless sourced.
```

### Reject

- Invented competitor facts.
- Overconfident market-size claims.
- Advice requiring private customer data.

## Case 4: Presentation Script and Memory Aid

Use for defense talks, demos, pitch decks, and technical presentations.

### Prompt Focus

```text
Review this sanitized slide-by-slide script for a 20-minute presentation.

Check:
- whether each slide has a clear job;
- where the speaker should slow down or compress;
- whether chart explanations say what to look at, what changes, and what it means;
- likely audience questions;
- memory-card cues.

Constraints:
- Do not invent results, names, institutions, or dates.
- Do not turn the talk into a written paper.
- Keep the speaker's scope and voice.
```

### Reject

- Adds unsupported results.
- Uses promotional language.
- Expands beyond the stated project.

## Case 5: Conflicting External AI Advice

If one model says "rewrite the whole section" and another says "only fix the transition", compare against the user's scope:

- If the user asked for a small polish, reject the broad rewrite.
- If the user asked for a full restructure, consider the broader option but still require evidence and local verification.
- Record the decision in the absorption table.
