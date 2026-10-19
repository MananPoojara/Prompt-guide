# Source ledger

Checked **2026-10-19** using primary documentation pages, engineering articles, and paper abstracts. Notes are concise paraphrases. The guides and prompt templates are original synthesis. This is a scoped research pass, not an exhaustive literature review.

## S01: OpenAI prompting

[Primary source](https://developers.openai.com/api/docs/guides/prompting) · Published/version: Living documentation · Checked: 2026-10-19

Supports: Task details, examples, versioned prompts, and evaluation.

Limit: Does not establish a universal best prompt.

## S02: Codex prompting

[Primary source](https://developers.openai.com/codex/prompting) · Published/version: Living documentation · Checked: 2026-10-19

Supports: Code-related prompts should name desired behavior, relevant context, and verification.

Limit: Documentation routes can redirect; recheck commands for your installed version.

## S03: Codex repository instructions

[Primary source](https://developers.openai.com/codex/guides/agents-md) · Published/version: Living documentation · Checked: 2026-10-19

Supports: Layered AGENTS.md discovery and configuration.

Limit: Applies to Codex; other hosts can load instructions differently.

## S04: Codex skills

[Primary source](https://developers.openai.com/codex/skills) · Published/version: Living documentation · Checked: 2026-10-19

Supports: Reusable workflows with metadata and selectively loaded instructions.

Limit: Installing a skill does not establish effectiveness.

## S05: OpenAI evaluation best practices

[Primary source](https://developers.openai.com/api/docs/guides/evaluation-best-practices) · Published/version: Living documentation · Checked: 2026-10-19

Supports: Task-specific evaluation and human calibration.

Limit: Hosted product availability is separate from evaluation methodology.

## S06: Effective context engineering for AI agents

[Primary source](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · Published/version: 2025-09-29 · Checked: 2026-10-19

Supports: Focused context, compaction, and structured notes for extended tasks.

Limit: Engineering guidance; no universal token ordering rule.

## S07: Building effective agents

[Primary source](https://www.anthropic.com/engineering/building-effective-agents) · Published/version: 2024-12-19 · Checked: 2026-10-19

Supports: Distinguishes predefined workflows from model-directed agents.

Limit: Article flags subsequent tooling changes.

## S08: Effective harnesses for long-running agents

[Primary source](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · Published/version: 2025-11-26 · Checked: 2026-10-19

Supports: Durable progress artifacts and incremental execution.

Limit: One published approach, not a mandatory architecture.

## S09: Demystifying evals for AI agents

[Primary source](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) · Published/version: 2026-01-09 · Checked: 2026-10-19

Supports: Trials, graders, traces, and actual environmental outcomes.

Limit: Evaluation quality depends on task coverage and grader validity.

## S10: Writing effective tools for agents

[Primary source](https://www.anthropic.com/engineering/writing-tools-for-agents) · Published/version: 2025-09-11 · Checked: 2026-10-19

Supports: Evaluate tool descriptions and responses on realistic tasks.

Limit: Tools still require correct implementation and authorization.

## S11: Bloom

[Primary source](https://www.anthropic.com/research/bloom) · Published/version: Publication year 2025 · Checked: 2026-10-19

Supports: Configurable automated behavioral evaluation and human-judge comparison.

Limit: Not evidence that self-grading guarantees correctness.

## S12: Automated Weak-to-Strong Researcher

[Primary source](https://alignment.anthropic.com/2026/automated-w2s-researcher/) · Published/version: Publication year 2026 · Checked: 2026-10-19

Supports: Agents propose, execute, and iterate in bounded research settings.

Limit: Benchmark design and overfitting remain limitations.

## S13: MCP architecture

[Primary source](https://modelcontextprotocol.io/docs/learn/architecture) · Published/version: Living specification; retrieved route 2026-07-28 · Checked: 2026-10-19

Supports: Host, client, server, and capability roles.

Limit: Connection is not evidence that every tool is usable.

## S14: Lost in the Middle

[Primary source](https://arxiv.org/abs/2307.03172) · Published/version: Revision 2023-11-20 · Checked: 2026-10-19

Supports: Context-position effects in studied retrieval and question-answering tasks.

Limit: Abstract-level review here; results cannot be generalized to every current model.

## S15: Large Language Models Cannot Self-Correct Reasoning Yet

[Primary source](https://arxiv.org/abs/2310.01798) · Published/version: Revision 2024-03-14 · Checked: 2026-10-19

Supports: Failures of intrinsic self-correction without external feedback in studied settings.

Limit: Abstract-level review here; not a dismissal of all feedback-driven correction.
