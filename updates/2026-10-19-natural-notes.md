# 2026-10-19 — More conversational notes, the same ceiling

[All updates](README.md)

The [naturalistic-note pilot](../labs/natural-notes/README.md) adds twelve synthetic dialogue/context cases to the prompt-comparison work. It covers conditional handovers, neighboring tasks, stale quotes, anchored dates, and conflicting decisions. Three variants were run three times each on the same twelve cases.

Every response scored 12/12. This remains a ceiling result, not proof that short instructions, rules, and examples are universally equivalent. The dataset is authored by the experiment designer, and no independent human annotation has been received.

The new [review packet and audit tool](../labs/natural-notes/review/README.md) distinguish missing review, disagreement, and uncertainty. Blank rows do not count as agreements; a model review cannot satisfy the human-review gate. Even a complete matching human submission requires maintainer review.

Readers can inspect all requests and outputs, recompute scores offline, and contribute annotations with their provenance stated. Seven review-tool tests and frozen-artifact checks passed. The complete runtime configuration is retained in the run manifest.

The next investigation changes the evidence available to the model: missing, stale, conflicting, or current documents. This targets retrieval and grounding failures rather than adding complexity to a saturated extraction test.
