# Reading the original artifacts

## Anthropic cookbook evaluator prompt

[Local original](vendor/anthropic-cookbook/evaluator_prompt.txt) · [Pinned upstream](https://github.com/anthropics/claude-cookbooks/blob/a162e0184e71b60290808a43961a6cbc8060123c/patterns/agents/evaluator_optimizer.ipynb)

**Provenance:** Published runnable example; published by `anthropics`. License: MIT. Retrieved 2026-10-19.

**Purpose:** Evaluate a candidate implementation against correctness, complexity, and style.

**How it runs:** Upstream evaluate() appends the original task and candidate code to this string, calls the model, and parses evaluation/feedback XML. The local experiment follows that assembly format.

**Boundary:** The criteria include having no further improvement suggestions. That can reject working code for subjective reasons. Model feedback is not an executable correctness test.

## Anthropic cookbook generator prompt

[Local original](vendor/anthropic-cookbook/generator_prompt.txt) · [Pinned upstream](https://github.com/anthropics/claude-cookbooks/blob/a162e0184e71b60290808a43961a6cbc8060123c/patterns/agents/evaluator_optimizer.ipynb)

**Provenance:** Published runnable example; published by `anthropics`. License: MIT. Retrieved 2026-10-19.

**Purpose:** Generate or revise code from a task and previous feedback.

**How it runs:** Upstream generate() combines this string with prior attempts and feedback, then the task. It parses response XML. The surrounding loop supplies the memory; this string alone does not persist it.

**Boundary:** The notebook asks for a thoughts field. It is generated explanatory text, not privileged access to a model’s internals. Do not treat it as proof of correctness. The published loop has no iteration cap; add one in a clearly labeled adaptation.

## Anthropic fresh-context evaluator

[Local original](vendor/anthropic-cwc/evaluator.md) · [Pinned upstream](https://github.com/anthropics/cwc-long-running-agents/blob/ad107a974bced5244f74dd283dbf2bfd3baee3a1/claude-code-config/.claude/agents/evaluator.md)

**Provenance:** Published event-demo subagent; published by `anthropics`. License: Apache-2.0. Retrieved 2026-10-19.

**Purpose:** Get an independent verdict on a builder’s claimed completion.

**How it runs:** Requires an acceptance specification, a Git baseline, and evidence files. Claude Code frontmatter selects tools; pasting frontmatter into an unrelated chat does not configure those tools.

**Boundary:** The upstream description explicitly says Bash is not a hard read-only boundary. Missing evidence is NEEDS_WORK. The event repository says it is a demo, not a turnkey maintained harness.

## Anthropic long-running handoff conventions

[Local original](vendor/anthropic-cwc/CLAUDE.md) · [Pinned upstream](https://github.com/anthropics/cwc-long-running-agents/blob/ad107a974bced5244f74dd283dbf2bfd3baee3a1/claude-code-config/.claude/CLAUDE.md)

**Provenance:** Published event-demo repository instructions; published by `anthropics`. License: Apache-2.0. Retrieved 2026-10-19.

**Purpose:** Carry progress and conventions across coding sessions.

**How it runs:** Requires PROGRESS.md, Git, project checks, and optionally the shipped hooks. The file describes how the agent should use those artifacts.

**Boundary:** A prompt instruction and a hook are different mechanisms. Copying CLAUDE.md alone does not install the verify-gate or commit hooks. A new user instruction still needs to be handled according to the host’s instruction hierarchy.

## OpenAI Codex compaction prompt

[Local original](vendor/openai-codex/compaction.md) · [Pinned upstream](https://github.com/openai/codex/blob/89461ea6833832b0551ce24ee32205824d5c108d/codex-rs/prompts/templates/compact/prompt.md)

**Provenance:** Published runtime prompt; published by `openai`. License: Apache-2.0. Retrieved 2026-10-19.

**Purpose:** Summarize task state for a continuation.

**How it runs:** Needs the actual conversation or task history as context. Its output is a handoff summary, not implementation work or a knowledge database.

**Boundary:** Compression can omit facts. Verify the resumed state against files and tests. This source file does not disclose every detail of deployed context management.

## OpenAI GPT-5.2 Codex base prompt

[Local original](vendor/openai-codex/gpt-5.2-codex_prompt.md) · [Pinned upstream](https://github.com/openai/codex/blob/89461ea6833832b0551ce24ee32205824d5c108d/codex-rs/core/gpt-5.2-codex_prompt.md)

**Provenance:** Published model-specific runtime prompt; published by `openai`. License: Apache-2.0. Retrieved 2026-10-19.

**Purpose:** Inspect published model-specific Codex behavior guidance.

**How it runs:** Written as agent-level instructions for Codex with filesystem and tool capabilities. It is useful for studying concrete editing, review, and communication expectations.

**Boundary:** The file names GPT-5.2 and its opening identifies a GPT-5-based agent. Do not paste it into another model and claim that identity or expect identical runtime behavior. We have not verified it is selected by today’s default runtime.
