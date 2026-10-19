# 2026-10-19 — Inspect what changes inside a small model

**For:** readers who understand tokens but want to distinguish embeddings, contextual representations, and attention.

The new [representation lab](../labs/representations/README.md) records two inputs with the same ` bank` token at the same position. Its lookup vector and input hidden state are identical; its final representation changes. The final cosine similarity is 0.990115, which is reported without interpreting it as a measure of understanding.

The offline visual exposes every attention head across all six blocks—144 matrices across two inputs—with numeric tables and explanations. Full vectors are retained. Browser controls and mobile width were tested; saved data checks verify causal masks, row sums, dimensions, and hashes. A separate Python environment reproduced all vectors and attention weights exactly.

**Evidence:** actual pinned DistilGPT2 execution, not proprietary-model internals. The [model chapter](../handbook/02-model-and-context.md) and roadmap now link this extension. The [core coverage audit](../CORE-COVERAGE.md) makes remaining requirements explicit before primarily switching to weekly maintenance.

**Action:** inspect a head, then compare it with another. Do not treat an attention weight as the causal explanation of an answer. No task-accuracy or word-sense benchmark was performed. Primary architecture and interpretability references appear beside the explanations in the lab.
