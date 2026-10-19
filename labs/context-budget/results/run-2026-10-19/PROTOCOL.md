# Context-budget demonstration — 2026-10-19

Predeclare an application capacity of 112 tokens with 16 reserved for output, leaving 96 input tokens. This is a deliberately small teaching budget, not DistilGPT2's actual maximum or a provider's chat accounting. Use the pinned DistilGPT2 tokenizer from model-mechanics; perform no inference.

Build a full plain-text request from instruction, one authoritative evidence paragraph, three distracting paragraphs, and a final question. Compare prefix-only truncation, suffix-only truncation, and whole-document packing that preserves the instruction/question and considers the evidence paragraph first. This priority is authored, not learned or discovered by a retriever. Recount the whole assembled text for each candidate instead of assuming separately tokenized lengths add exactly.

Save exact token IDs, decoded text, retained-segment checks, selected/omitted document IDs, model revision and code hashes. Required segments that exceed the budget must raise an error rather than disappear. The demonstrated result concerns which bytes/tokens reach inference; no model-answer outcome is inferred from it.
