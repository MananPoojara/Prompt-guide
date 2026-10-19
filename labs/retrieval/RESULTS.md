# Recorded retrieval results

Executed 2026-10-19. Ten authored evaluation questions; two development questions excluded from this summary. No configuration was tuned after viewing scores.

| Method | Chunks | Document hit@1 | Complete evidence@1 | Complete evidence@3 | Mean retrieved characters@3 |
|---|---:|---:|---:|---:|---:|
| bm25-48 | 67 | 5/10 | 2/10 | 3/10 | 708 |
| dense-48 | 67 | 9/10 | 1/10 | 4/10 | 737 |
| bm25-128 | 21 | 7/10 | 4/10 | 5/10 | 1816 |
| dense-128 | 21 | 10/10 | 5/10 | 10/10 | 1794 |
| dense-254 | 10 | 10/10 | 10/10 | 10/10 | 3531 |

## Per-question complete evidence coverage at top 3

| Question | bm25-48 | dense-48 | bm25-128 | dense-128 | dense-254 |
|---|---|---|---|---|---|
| double-write | no | no | no | yes | yes |
| key-conflict | yes | yes | yes | yes | yes |
| old-secret | no | no | no | yes | yes |
| event-ack | no | no | no | yes | yes |
| empty-page | no | no | yes | yes | yes |
| throttle-delay | no | no | yes | yes | yes |
| safe-logs | no | yes | no | yes | yes |
| worker-exit | yes | yes | yes | yes | yes |
| remove-fields | no | no | no | yes | yes |
| cache-write | yes | yes | yes | yes | yes |

These counts measure retrieval, not generated-answer correctness. Equal top-k uses different amounts of text. Larger windows cover longer reference spans more easily; this is a consequential part of the comparison, not a controlled equal-token-budget experiment. The full ranks, scores, source offsets, and actual vectors are in [data.json](results/pilot-2026-10-19/data.json).
