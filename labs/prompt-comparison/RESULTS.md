# Result: all three variants tied

Executed 2026-10-19. **All three arms scored 16/16 in every repetition.** This pilot did not observe an accuracy benefit from adding explicit rules or four examples.

| Arm | Trial 1 | Trial 2 | Trial 3 | Case observations | Median CLI duration |
|---|---:|---:|---:|---:|---:|
| short | 16/16 | 16/16 | 16/16 | 48/48 | 15.502 s |
| rules | 16/16 | 16/16 | 16/16 | 48/48 | 19.557 s |
| examples | 16/16 | 16/16 | 16/16 | 48/48 | 18.894 s |

**Counts are descriptive:** each arm made three calls containing the same 16 notes. The 48 observations are correlated and do not represent 48 independent trials or 48 distinct tasks.

## What the checks found

All nine responses followed the strict JSON contract. There were zero schema failures, wrong owner/deadline fields, and execution failures in the completed low-effort run. Every category scored 6/6 observations per arm. Paired comparisons had zero improvements and zero regressions; all 48 paired case observations passed in both arms. See [scores.json](results/pilot-low-2026-10-19/scores.json) for case-level results.

## What this tells us

The short instruction was sufficient for this model on these deliberately explicit synthetic notes. This dataset reached a ceiling: its scores cannot distinguish the prompt variants. The result does not establish that examples are useless, that the three approaches are equivalent on other tasks, or that this system is perfectly reliable.

The dataset was authored and audited by the same assistant that designed the prompts. Held-out cases were excluded from demonstrations and outcome-driven tuning, but they were not independently annotated or hidden from the experiment designer. Both the notes and the scoring policy favor clear, single-record extraction. Real meeting notes may contain much less explicit language.

No confidence interval is reported because treating the pooled observations as independent would overstate the evidence. Three repetitions expose only limited variability. All runs used one model, fixed note order, and a rotating but nonrandom arm order.

## Runtime and setup failure

The completed run used Codex CLI 0.163.0, gpt-6.1-sol, reasoning effort low, fresh ephemeral sessions, ignored user configuration, read-only sandbox, and separate empty working directories. Full commands and durations are in the [manifest](results/pilot-low-2026-10-19/manifest.json). Codex built-in runtime instructions remain part of the experiment. No model sampling seed or temperature was controlled.

The earlier [setup attempt](results/pilot-2026-10-19/manifest.json) requested unsupported reasoning effort none. Five calls returned endpoint errors before the runner was interrupted during a sixth request. No successful model answer was discarded. The aborted attempt and frozen original protocol are retained separately, and the amended protocol was frozen before the successful run.

Durations include CLI startup and network/runtime overhead. Logs include model-list refresh timeout diagnostics; completed requests still returned successfully. These three observations per arm do not support a reliable speed ranking, and account billing was not measured.

## Inspect and reproduce

- [Protocol and rubric](PROTOCOL.md): fixed interpretation rules, scoring, and limitations.
- [Dataset](dataset.json): all notes, expected values, categories, and author rationales.
- [Completed run](results/pilot-low-2026-10-19): nine assembled requests, raw outputs, logs, frozen inputs, and scores.
- [Offline verification](check_saved.py): hashes, assembly, schedule, artifact presence, and score recomputation.

The scorer/runner tests cover invalid JSON, duplicate keys, invalid dates, missing/extra/out-of-order records, wrong fields, timeout/error retention, paired changes, and overwrite protection. Fourteen tests passed; standard-library trace measured 91% line coverage for experiment.py in the offline tests. Mocked transport tests are labeled in their code and are separate from the real model run.

## Next useful experiment

Obtain independently reviewed, more natural notes and reserve a new held-out set before further prompt changes. Include indirect assignments, temporal ambiguity, cross-note references, and genuine disagreement over the gold labels. Freeze the revised rubric before running comparisons. Preserve this ceiling result rather than quietly replacing it with a more favorable subset.
