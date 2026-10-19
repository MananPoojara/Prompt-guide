# Inspect the work

Start with an artifact, trace how it was used, and check the outcome. Every case identifies whether its evidence is an upstream report or a local execution.

| Case | What you can inspect | What it establishes |
|---|---|---|
| [Anthropic’s game-maker experiment](anthropic-game-maker.md) | Engineer’s exact task prompt, workflow graph, reported comparison | Same task prompt used with different orchestration; not a prompt-only improvement |
| [Anthropic evaluator prompt in Codex](evaluator-loop/README.md) | Exact original prompt, request assembly, defective and correct code, repeated outputs | Local evidence about a published evaluator under a different runtime |
| [Evidence-gated completion](evidence-gate.md) | Original reviewer, conventions, and hook source | Difference between asking for proof and enforcing an evidence-read check |
| [What reaches the model](request-to-result.md) | Input assembly and tool-return sequence | How prompts, skills, plugins, MCP, memory, and the harness fit together |
| [Search fix](../labs/search-fix/README.md) | Exact prompt, original code, resulting code, unchanged tests | One verified coding change |
| [A prompt comparison that tied](../labs/prompt-contract/README.md) | Both prompts and actual outputs | More explicit instructions did not improve these four easy cases |

The first two source categories matter: **published** means the original publisher released it; **executed here** means this repository contains our run evidence. Neither label means universally effective.
