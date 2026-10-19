# Recorded outcomes: equal evidence ceiling, different failures

[Explanation](README.md) · [Protocol](PROTOCOL.md) · [Raw recording](results/pilot-2026-10-19/data.json)

Recorded 2026-10-19. Six evaluation questions per method, one answer call per question. Two development retrieval rows per method are retained but excluded from these counts. All twelve processes completed successfully.

| Method | Reference covered | Correct short answer | Narrow supported answer | Abstentions | Mean evidence tokens | Summed call seconds |
|---|---:|---:|---:|---:|---:|---:|
| bm25 | 5/6 | 5/6 | 4/6 | 1 | 357.8 | 97.601 |
| dense | 4/6 | 5/6 | 3/6 | 1 | 359.8 | 36.196 |

Every response passed the JSON contract. Durations include CLI/service overhead and are descriptive, not a stable speed ranking. BM25 calls ran first, followed by dense calls; order and service conditions can confound timing comparisons. Evidence tokens use MiniLM, not generator billing. Billing was not collected.

| Method | Question | Reference covered | Correct value | Quote in cited chunk | Full reference in quote | Abstained |
|---|---|---|---|---|---|---|
| bm25 | [no-cancel](results/pilot-2026-10-19/bm25-no-cancel.output.txt) | No | No | No | No | Yes |
| bm25 | [progress-type](results/pilot-2026-10-19/bm25-progress-type.output.txt) | Yes | Yes | Yes | Yes | No |
| bm25 | [root-scheme](results/pilot-2026-10-19/bm25-root-scheme.output.txt) | Yes | Yes | Yes | Yes | No |
| bm25 | [schema-obligation](results/pilot-2026-10-19/bm25-schema-obligation.output.txt) | Yes | Yes | Yes | Yes | No |
| bm25 | [version-mismatch](results/pilot-2026-10-19/bm25-version-mismatch.output.txt) | Yes | Yes | Yes | No | No |
| bm25 | [internal-error](results/pilot-2026-10-19/bm25-internal-error.output.txt) | Yes | Yes | Yes | Yes | No |
| dense | [no-cancel](results/pilot-2026-10-19/dense-no-cancel.output.txt) | Yes | Yes | Yes | Yes | No |
| dense | [progress-type](results/pilot-2026-10-19/dense-progress-type.output.txt) | No | Yes | Yes | No | No |
| dense | [root-scheme](results/pilot-2026-10-19/dense-root-scheme.output.txt) | Yes | Yes | Yes | Yes | No |
| dense | [schema-obligation](results/pilot-2026-10-19/dense-schema-obligation.output.txt) | No | No | No | No | Yes |
| dense | [version-mismatch](results/pilot-2026-10-19/dense-version-mismatch.output.txt) | Yes | Yes | Yes | No | No |
| dense | [internal-error](results/pilot-2026-10-19/dense-internal-error.output.txt) | Yes | Yes | Yes | Yes | No |

## Inspect the failures

- **Cancellation:** BM25 selected other lifecycle/cancellation passages but missed the explicit prohibition on cancelling `initialize`; the model abstained. Dense retrieval selected the required statement and returned a supported answer.
- **Tool-schema obligation:** dense retrieval missed the explicit server obligation and the model abstained. BM25 included it and returned `MUST` with a supporting quote.
- **Progress-token types:** dense retrieval selected a fragment beginning `s **MUST** be a string or integer value`. The model returned the correct types and cited that real fragment, but the quote omits its subject. The complete-reference check rejects it. This is why correct values and complete supporting statements are separate measurements.
- **Version mismatch:** both methods contain the full reference across selected chunks, but the generated single-chunk quote starts with `client does not support` rather than `If the client does not support`. The correct answer and quote-provenance checks pass; the full-reference check fails. This strict authored rubric is sensitive to chunk boundaries and quotation completeness, not just semantic correctness.

No outputs or reference labels were repaired after seeing these outcomes. A future semantic grader could judge the version-mismatch fragments differently, but that would require a new documented rubric and ideally independent review. The present results retain the original rule.

## Verification and limits

Seven boundary tests pass, covering budget skipping/recounting, invalid budgets, valid answers, fabricated quotes, wrong citations, wrong values, abstention, and invalid schemas. The 30-statement packing/grading module has 100% line coverage in this test run. Coverage is a code-execution measure, not proof that the rubric is adequate.

The offline verifier recalculates rankings and source coverage, checks exact source/code hashes, reconstructs requests, and regrades all outputs. Cached-tokenizer replay additionally reproduced the selected chunks, packet token IDs, and greedy packing decisions. No fresh model generation is implied by replay.

These six authored tasks and single calls do not establish general retrieval superiority. They do demonstrate that a winner on the earlier fictional corpus need not win on this historical real-document set. No causal attribution to retrieval alone, independent reviewer approval, or production-readiness claim is made.
