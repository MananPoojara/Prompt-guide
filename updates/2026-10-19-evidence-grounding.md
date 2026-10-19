# 2026-10-19 — Retrieval can fail even when the model behaves appropriately

[All updates](README.md)

The [evidence-availability lab](../labs/evidence-grounding/README.md) keeps three questions and the answering prompt fixed while changing the supplied documents. Five conditions cover missing evidence, a stale lexical-search result, a current result, conflicting current sources, and an untrusted instruction-like comment.

Across two calls per condition, the model handled all six question observations per condition according to the rubric. But resolution differed: no evidence and the superseded draft resolved zero questions; the current plan resolved all six observations. The conflict condition resolved only the shared undecided registration state. Correct abstention is kept separate from actually answering the user's question.

All source documents are fictional and explicitly labeled by authority/status. This is an inspectable retrieval demonstration, not a general robustness benchmark. The injected comment represents one simple attack, not a comprehensive security evaluation.

The [scoring amendment](../labs/evidence-grounding/SCORING-AMENDMENT.md) documents a citation edge case and malformed-status bug found by unit tests during recording. Original scores and corrected re-scores are retained; totals did not change. Eleven tests and offline artifact checks passed.

Readers can inspect the selected evidence and each response locally. The next step is a bounded agent that chooses retrieval actions and saves its execution state, using the same small corpus.
