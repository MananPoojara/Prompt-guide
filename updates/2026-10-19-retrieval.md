# 2026-10-19 — A correct document hit can still omit the answer

**For:** developers building a retrieval-augmented assistant.

The new [developer retrieval lab](../labs/retrieval/README.md) compares BM25 with a pinned MiniLM encoder over ten fictional platform documents. It records 48- and 128-token windows and a first-254-token baseline. All vectors, rankings, source offsets, and reference spans are retained.

Small-window embedding search ranked the correct document first for 9/10 evaluation questions, but covered the complete reference span in its top three chunks for only 4/10. The 128-token embedding condition reached 10/10 top-three coverage using more text. The largest-window baseline also succeeded; it remains in the report. Exact-span coverage is narrower than answerability, and no generated-answer accuracy was measured.

**Evidence:** actual CPU encoder execution, ten unit tests, offline regrading, and a separate-environment reproduction matching every vector, rank, and evidence metric. The dataset and labels are authored and have no independent review. A corrected Python module-name collision is disclosed in the verification record.

**Action:** inspect the returned text before changing your answer prompt. Compare complete evidence, not only document IDs, and report the context-volume tradeoff. The [developer lab path](../labs/README.md), context chapter, main README, and roadmap now connect this experiment to model mechanics and grounded answering.
