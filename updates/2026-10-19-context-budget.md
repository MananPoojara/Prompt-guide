# 2026-10-19 — Check what survives the context budget

**For:** developers assembling model requests from multiple documents.

The [context-budget lab](../labs/context-budget/README.md) records a 203-token plain-text request under a deliberately small 96-token input budget. Prefix truncation retains evidence but loses the question. Suffix truncation retains the question but loses both instruction and evidence. A whole-document packer retains all three in 62 tokens.

This uses actual tokenization with a pinned tokenizer and no inference. The budget is an application teaching choice, not a provider context limit. The evidence priority is authored; the experiment does not establish retrieval quality or answer accuracy.

**Evidence:** exact token IDs, decoded slices, retained-segment checks, source hashes, and seven passing unit tests. The offline checker verifies the recorded artifacts; rerunning the recorder verifies tokenization. No model output is fabricated.

**Action:** inspect the final request, preserve required segments, reserve output space under the actual interface's accounting, and fail visibly when mandatory content cannot fit. The model chapter, developer path, roadmap, and coverage audit now link the demonstration.
