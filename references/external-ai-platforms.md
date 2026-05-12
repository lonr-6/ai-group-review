# External AI Platform Notes

These notes are intentionally generic. Web UI details change often.

## Provider Loop

For each requested AI site:

1. Open or select the site.
2. Confirm the user is logged in.
3. Confirm the requested model or mode if the UI shows it.
4. Paste the approved prompt or chunk.
5. Submit.
6. Wait for completion.
7. Save raw text locally with metadata.
8. Record blocker if anything fails.

## Manual Fallback

Browser automation can fail because web apps change selectors, block paste, require CAPTCHA, or need manual model selection. If automation fails:

- ask the user to paste the prompt manually or refresh the page;
- keep the same prompt packet and archive structure;
- record that the response was collected manually.

Do not bypass CAPTCHA, login, paywalls, or platform limits.

On Windows, clipboard writes may occasionally leave old content in the browser paste buffer. After pasting, verify the first lines or character count before sending. If the pasted content is stale or incomplete, reset the clipboard with a more reliable method, paste manually, or ask the user to paste the approved packet.

## Provider Metadata to Record

- Provider name.
- URL.
- Visible model or mode.
- Prompt packet version.
- Round number.
- Submission time.
- Completion time if known.
- Response status: complete, truncated, blocked, empty, error, manual.
- Notes: login issue, CAPTCHA, model unavailable, rate limit, paste limit, user manually entered, or response continued.

## Long Prompt Handling

If a prompt is too long:

1. Split by sections or paragraphs.
2. Send numbered chunks.
3. In all non-final chunks, ask the model to read and acknowledge only.
4. In the final chunk, ask for the actual review.
5. Archive all chunk prompts.

## Model Role Diversity

When useful, give different providers different review lenses instead of asking all of them the same broad question. Examples:

- One model checks logic and missing assumptions.
- One model checks style and clarity.
- One model checks risk and privacy.
- One model checks implementation details or failure modes.

Use identical prompts when the goal is direct comparison.
