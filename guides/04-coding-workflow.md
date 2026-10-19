# 4. From vibe coding to a change you can trust

Natural language can start the work. Acceptance criteria, inspection, and tests make the result reviewable. Use this workflow on an existing repository; substitute its actual commands and conventions.

## Stage 1: Inspect

```text
Read the repository instructions and trace how product search reaches the UI.
Identify the implementation, tests, and commands relevant to changing search
normalization. Cite file paths. Do not edit yet. List any ambiguity that
would change observable behavior.
```

Checkpoint: follow the cited files yourself. If the agent describes nonexistent modules, repair its context before asking for implementation.

## Stage 2: Specify and implement

Use the [search normalization prompt](01-prompt-contract.md). For a larger feature, write a small vertical slice with a user-visible acceptance check before adding optional features.

```text
Implement the agreed search normalization behavior. Preserve the existing
public interfaces and sorting rules. Add meaningful checks for case and
whitespace normalization and run the relevant regression tests. If the
existing behavior conflicts with the agreement, show the conflict before
choosing a new product behavior.
```

Checkpoint: inspect the diff. Tests should exercise the requested behavior, not simply repeat the implementation's code structure.

## Stage 3: Review against evidence

```text
Review the diff against the acceptance criteria. Look for concrete regressions,
missing edge cases, and unsupported claims of completion. For each finding,
show the triggering input, file location, and consequence. Verify findings
where possible. If no issue is found, report the limits of the review.
```

Checkpoint: a reviewer can share the author's blind spots. Retain executable tests and human review of product decisions.

## Stage 4: Handoff

```text
Summarize the resulting behavior, files changed, commands actually executed,
and their exit status. Separate verified results from checks that could not
run. Include any remaining user-facing limitation and the next concrete step.
```

## When it goes wrong

| Observation | Recovery |
|---|---|
| Agent keeps rewriting unrelated code | Restate scope and inspect the diff before more work |
| Test cannot start | Resolve setup failure; do not report a product pass |
| Test passes but the page is broken | Exercise the real user flow in the browser |
| Agent changes the test to accept a bug | Compare test assertions against the original requirement |
| Context is exhausted | Save a factual handoff and resume with state verification |

For a UI feature, include loading, empty, error, keyboard, and narrow-screen states when relevant. For persistence, restart and confirm the data survives. For an external integration, inspect the remote outcome rather than trusting “sent successfully.”

The prompts above are teaching examples. The [search-fix lab](../labs/search-fix/README.md) includes an executed coding task with unchanged tests and saved before-and-after results. The [Codex lab](../labs/prompt-contract/README.md) records an actual, narrower prompt/output experiment. Do not use its score as proof of software engineering performance.

Public reference: [OpenAI's Codex prompting examples](https://developers.openai.com/codex/prompting). Our checkpoints are original applications of observable task verification.

Next: [Tools, skills, and MCP](05-tools-skills-mcp.md).
