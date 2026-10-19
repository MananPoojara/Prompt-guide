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

## S16: Anthropic evaluator–optimizer implementation

[Pinned notebook](https://github.com/anthropics/claude-cookbooks/blob/a162e0184e71b60290808a43961a6cbc8060123c/patterns/agents/evaluator_optimizer.ipynb) · Checked: 2026-10-19.

Supports: exact published generator/evaluator strings, request assembly, XML parsing, and feedback loop. Root license inspected: MIT. Exact strings and notebook retained under originals/vendor/anthropic-cookbook.

Limit: official runnable example, not evidence of a particular engineer's private daily usage. Local runs use Codex rather than the upstream Anthropic API settings.

## S17: Anthropic Code with Claude long-running primitives

[Pinned repository](https://github.com/anthropics/cwc-long-running-agents/tree/ad107a974bced5244f74dd283dbf2bfd3baee3a1) · Checked: 2026-10-19.

Supports: original evaluator instructions, handoff conventions, and example evidence-read hooks. License inspected: Apache-2.0. Repository explicitly describes an event demo and says it is not maintained.

Limit: source inspected; full runtime integration not tested here. Hook source documents bypasses and limited evidence matching.

## S18: OpenAI Codex published prompt files

[Pinned repository](https://github.com/openai/codex/tree/89461ea6833832b0551ce24ee32205824d5c108d) · Checked: 2026-10-19.

Supports: exact compaction and GPT-5.2 Codex base prompt file contents. Apache-2.0 license and NOTICE retained.

Limit: file existence does not prove selection by the current deployed default. This is public source, not a disclosure of all private runtime instructions.

## S19: Anthropic Labs engineer's game-maker experiment

[First-person report](https://www.anthropic.com/engineering/harness-design-long-running-apps) · Published: 2026-03-24 · Checked: 2026-10-19.

Supports: named engineer, published task prompt, and a reported solo-versus-harness comparison. See cases/anthropic-game-maker.md for the scoped account.

Limit: not rerun locally, and the comparison changes orchestration rather than isolating prompt wording.

## S20: Transformer architecture background

[Attention Is All You Need](https://arxiv.org/abs/1706.03762) · Submitted: 2017-06-12 · Checked: 2026-10-19, abstract-level review.

Supports: the original attention-based Transformer architecture proposal.

Limit: does not establish the architecture or internal reasoning mechanism of every contemporary proprietary model.

## S21: MCP Python SDK client, version 2 interface

[Primary source](https://py.sdk.modelcontextprotocol.io/client/) · Published/version: Living documentation, example pins mcp 2.3.0 · Checked: 2026-10-19

Supports: Client lifecycle, subprocess transport, tool discovery/calls, and structured results. Local implementation and successful/error cases are independently exercised in examples/mcp-notes/.

Limit: This is an SDK/API source, not evidence of model tool-selection quality. The recorded protocol version is 2026-07-28; older examples can use incompatible APIs.

## S22: Claude Code plugin packaging

[Primary source](https://code.claude.com/docs/en/plugins) · Published/version: Living documentation · Checked: 2026-10-19

Supports: A plugin packages components; the manifest identifies it, skills are namespaced, and local directory loading supports development. Installed CLI help and validation supplement the documentation.

Limit: The local sample is authored here. Static validation does not establish a successful model-driven invocation.

## S23: DistilGPT2 model and generation mechanics

[Pinned model card](https://huggingface.co/distilbert/distilgpt2/tree/2290a62682d06624634c1f46a6ad5be0f47f38aa) · [Generation reference](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation) · Checked: 2026-10-19

Supports: model identity and licensing; library meanings of temperature, greedy selection, and top-k sampling. The model-mechanics lab independently records actual tokenizer output and CPU generation using a pinned revision and package versions.

Limit: an older text-completion model does not establish behavior of current proprietary chat assistants. The browser visual recalculates probabilities from saved logits and displays recordings; it does not perform inference.
