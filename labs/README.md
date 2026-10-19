# Advanced labs for developers

[Main guide](../README.md) · [Foundations](../START-HERE.md) · [Full roadmap](../ROADMAP.md)

Build judgment by following the input through an actual system. Each lab includes a concrete question, runnable implementation, retained evidence, checks, and limits. You can inspect saved results without a model account; rerunning inference has separate requirements.

| Step | Build or inspect | What you learn to diagnose |
|---|---|---|
| 1 | [Tokens and sampling](model-mechanics/README.md) | Tokenization, probability distributions, and generation settings |
| 2 | [Embeddings and attention](representations/README.md) and [context budgets](context-budget/README.md) | Stored vectors versus contextual computation; limits of attention pictures |
| 3 | [Controlled prompt comparison](prompt-comparison/README.md) and [natural notes](natural-notes/README.md) | Fair comparisons, held-out cases, ceiling results, and missing independent review |
| 4 | [Bounded output repair](output-repair/README.md) | JSON validity versus evidence correctness; stop when evidence is absent |
| 5 | [A developer-document retriever](retrieval/README.md) | Lexical versus embedding search, chunk boundaries, and evidence coverage |
| 6 | [Evidence-grounded answering](evidence-grounding/README.md) | Missing, stale, conflicting, and instruction-like evidence; abstention versus resolution |
| 7 | [Memory lifecycle](memory-lifecycle/README.md) | Corrections, revision conflicts, expiry, retraction, and current context |
| 8 | [A bounded tool loop](bounded-agent/README.md) and [controlled failures](agent-recovery/README.md) | Model decisions, host constraints, checkpoints, and replay |
| 9 | [Single call, workflow, or agent](workflow-comparison/README.md) | Equal-task comparisons, ties, call overhead, and conflict detection |
| 10 | [Exact-action approval](action-approval/README.md) | Binding review to a proposal and rejecting changed inputs |
| 11 | [Operational evaluation](../evaluation/README.md) and [uncertainty](eval-uncertainty/README.md) | Process success versus answer correctness, regression checks, and accounting gaps |

For coding agents, also inspect the [saved search fix](search-fix/README.md), [evaluator/repair case](../cases/evaluator-loop/README.md), and [executed local MCP connection](../examples/mcp-notes/README.md).

## What makes these advanced?

The emphasis is on engineering decisions you can inspect: which evidence reached the model, what the runtime allowed, where a metric can mislead, and whether a change survives a controlled comparison. A more complicated prompt is not automatically a better technique. A successful small experiment is not a deployment guarantee.

The next additions include example-selection/decomposition comparisons, broader adversarial cases, and independently reviewed evaluation. The [coverage audit](../CORE-COVERAGE.md) distinguishes those gaps from delivered material. Independent human review remains pending; authored labels are labeled accordingly.
