# Recorded result: all five conditions tied

[Lab explanation](README.md) · [Frozen protocol](PROTOCOL.md) · [Raw manifest](results/pilot-2026-10-19/manifest.json)

Recorded 2026-10-19. Every condition passed 10/10 notes in both repetitions. All final batches passed the strict schema; all twelve model processes succeeded. This pilot found no final-answer improvement from the examples, example order, or additional stage.

| Condition | Repetition 1 | Repetition 2 | Exact batches | Model calls | Summed CLI seconds | Submitted characters across calls |
|---|---:|---:|---:|---:|---:|---:|
| none | 10/10 | 10/10 | 2/2 | 2 | 16.071 | 6348 |
| simple | 10/10 | 10/10 | 2/2 | 2 | 15.900 | 6950 |
| boundary | 10/10 | 10/10 | 2/2 | 2 | 15.900 | 7398 |
| reversed | 10/10 | 10/10 | 2/2 | 2 | 14.269 | 7398 |
| decomposed | 10/10 | 10/10 | 2/2 | 4 | 68.529 | 19450 |

These are observed sequential run durations, not controlled speed rankings. Input characters are not token usage or billed cost. The two-stage condition includes both calls and its intermediate text. It used four calls across two repetitions, versus two calls for each direct condition.

## Paired outcomes

| Comparison | Improved cases | Regressed cases | Both passed | Both failed |
|---|---:|---:|---:|---:|
| simple → boundary | 0 | 0 | 20 | 0 |
| boundary → reversed | 0 | 0 | 20 | 0 |
| boundary → decomposed | 0 | 0 | 20 | 0 |

The twenty observations in each row reuse ten notes across two batches. They are not twenty independent tasks. A ceiling result cannot establish that the techniques are equivalent or that ordering never matters. The shared rules may already be sufficient for this limited task.

## Inspect the intermediate artifacts

- [First ledger](results/pilot-2026-10-19/1-decomposed-ledger.output.txt) → [exact second-stage request](results/pilot-2026-10-19/1-decomposed-final.input.txt) → [final answer](results/pilot-2026-10-19/1-decomposed-final.output.txt).
- [Second ledger](results/pilot-2026-10-19/2-decomposed-ledger.output.txt) → [exact second-stage request](results/pilot-2026-10-19/2-decomposed-final.input.txt) → [final answer](results/pilot-2026-10-19/2-decomposed-final.output.txt).

A post-run provenance inspection found 33 event quotes in repetition 1, with 0 nonliteral quotes, 31 event quotes in repetition 2, with 0 nonliteral quotes. Each checked quote was compared with its own original note. This diagnostic was not the predeclared final-answer metric and does not validate event interpretation or completeness.

The first ledger preserves the meeting-date anchor separately from the export date for the year-boundary question. It also labels the instruction-like log values as `proposed` events. That latter label blurs an untrusted command with an ordinary unaccepted proposal: the current event vocabulary has no dedicated trust/source-authority field. The final answer remained correct in this run, but that does not prove the intermediate representation preserves every important distinction. A follow-up should explicitly represent authority and test whether an untrusted instruction can be promoted into an accepted event. The saved ledger is unchanged.

## What to do with a tie

For this task, the direct rules-only condition achieved the same final scores with fewer calls than decomposition. That supports retaining the simpler baseline here. It does not show that demonstrations or decomposition are generally useless.

A useful next experiment would predeclare a task where intermediate evidence can be independently validated, include harder naturalistic examples and independent labels, and measure whether decomposition fixes a specific failure. Do not keep modifying these published notes until a preferred technique wins.

## Verification

Five unit tests passed; the assembly/scoring module reached 100% line coverage across 41 statements. The saved-run verifier reconstructs all twelve inputs, checks frozen source hashes, confirms the declared schedule, and regrades all final outputs. It runs no model calls and does not grade intermediate semantics. Independent human label and reader review remain pending.
