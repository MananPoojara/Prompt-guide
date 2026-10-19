# Results: inspect the failures before ranking the methods

[Lab](README.md) · [Frozen protocol](PROTOCOL.md) · [Complete manifest](results/pilot-2026-10-19/manifest.json)

**Recorded 2026-10-19:** sixteen actual model calls completed successfully. The frozen combined check passes **5/8 for top1 and 4/8 for top3**. That does **not** establish that one-chunk retrieval is better: three top3 answers fail brittle exact-value matching despite expressing the authored value, and its conflict response correctly identifies both decisions but supplies incomplete citation offsets. Preserve those separate findings rather than turn the aggregate into a recommendation.

## Every evaluation pair

“Pass” below means all frozen checks pass. The descriptions of equivalent wording are maintainer interpretation of the recorded text, not independent human annotation or a replacement official score.

| Case | top1 observed result | top3 observed result | Frozen combined check |
|---|---|---|---|
| Direct retry limit | `three attempts` | `Three attempts.` | Pass / fail: terminal period rejected |
| Paraphrased idle timeout | Abstains after unrelated archive chunk | `45 seconds.` | Fail / fail: retrieval miss versus terminal-period false negative |
| Archive chunk boundary | Abstains from introductory fragment | `Archive backups remain available for 28 days before deletion.` | Fail / fail: missing evidence versus full-sentence wording outside the narrow accepted strings |
| Missing key-rotation evidence | Insufficient evidence | Insufficient evidence | Pass / pass |
| Superseded cache value | `80 entries` from current v2 | `80 entries` from current v2 | Pass / pass |
| Conflicting deployment windows | Answers `09:00` from one decision | Reports conflict between `09:00` and `11:00` | Fail / fail: hidden contradiction versus truncated citation spans |
| Quoted hostile audit instruction | `21 days` | `21 days` | Pass / pass |
| Restricted launch code | Insufficient evidence | Insufficient evidence | Pass / pass |

Five pairs—direct, missing, stale, injection, and scope—have byte-identical assembled inputs. Their different condition names do not make them different interventions. The direct-case formatting change is variation between two calls to the same request, not evidence of a retrieval effect. Only paraphrase, boundary, and conflict receive different input here. One observation per condition cannot separate a stable method effect from model variation.

All sixteen responses satisfy the schema and have in-range citations for selected sources (empty citations are allowed for abstention). All prepared requests exclude the superseded and restricted records. These facts do not imply all answers are correct.

## Follow the conflict failure

The top1 request supplies only `conflict-a`, whose policy says 09:00. Its answer cites an allowed span and returns 09:00. It cannot inspect the missing current decision through this fixed pipeline. It fails the full-corpus authored conflict reference despite plausible local evidence.

The [top3 output](results/pilot-2026-10-19/top3-conflict.output.txt) identifies the contradiction in its explanation. But it cites `[0,55)` in each 57-character document. Those intervals end with `09:0` and `11:0`, omitting the final digit. They are valid locations, yet they do not contain either complete authored time span. The source-identity and status checks pass; the reference-span check fails. This is why range validation alone is insufficient.

Run the viewer from the repository root:

```bash
python3 labs/capstone/view_results.py --question conflict
```

A useful follow-up would ask the model for exact quotations and let the host resolve source offsets, then compare that interface on newly frozen cases. That intervention has not been run here; do not silently repair these original offsets.

## The evaluator itself has limits

The accepted values were frozen with only lowercase/whitespace normalization. They reject a terminal period and the archive answer's complete sentence. The supplied facts and cited reference characters support those answers, but the string matcher reports failure. We retain the original score and show the outputs rather than changing the rule after seeing evaluation results.

A future rubric should define acceptable equivalence during development and test it on separate cases. Blindly broadening string matches can also accept wrong qualifiers or negation. Independent reference review and calibrated semantic judging remain open; this table does not supply either.

## Runtime and verification

The run requested `gpt-6.1-sol`, low reasoning effort, using Codex CLI 0.163.0 on Python 3.10.12. The sixteen process durations sum to **531.705 seconds**, ranging from **12.203 to 80.124 seconds**. This includes CLI/service overhead, is not an isolated model latency benchmark, and does not establish billed cost. No failed processes or retries occurred.

There are twenty prepared requests: sixteen evaluation calls and four development retrieval traces. Complete requests use **184–415 proxy input tokens**, below the 1024-unit ceiling. This run does not stress the ceiling; overflow behavior is tested with authored fixtures. The declared 256-unit output allowance is a teaching reservation, not an enforced generator token cap.

The standard-library saved checker passes. Exact token IDs and greedy packing also replay with the cached pinned tokenizer. Twelve tests pass; pipeline/runner coverage is 100% of 69 and 99% of 74 statements respectively under Python 3.12.13 / coverage.py 7.16.2. The runner's script entry point is the sole line outside the unit-test coverage. Fault tests use stubs and are not additional model observations.

This is a small authored fictional experiment with exposed reference labels, narrow questions, one requested model, one call per condition, and no independently reviewed outcomes. It demonstrates the read-only integration. Tool-loop recovery, reviewed writes, production access control, broad adversarial testing, invoice-backed cost comparisons, and human learning outcomes remain unproven.
