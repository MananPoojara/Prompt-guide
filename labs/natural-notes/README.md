# Naturalistic notes: another ceiling, not a winner

[First controlled pilot](../prompt-comparison/README.md) · [Protocol](PROTOCOL.md) · [Independent review packet](review/README.md)

The first pilot's short, explicit notes were too easy to distinguish three prompt variants. This follow-up introduces twelve new synthetic notes with dialogue, conditional commitments, nearby tasks, stale quotes, relative dates, and conflicting current decisions. It retains eight development examples from the first dataset, with four shown only in the examples arm.

The scenarios are authored, not collected from real meetings. The same assistant designed the prompts and gold labels. The source [dataset](dataset.json) includes every note, answer, and rationale. No independent human reviewer has supplied labels.

## The comparison

The three prompts are [short](prompts/short.txt), [rules](prompts/rules.txt), and [rules with examples](prompts/examples.txt). Each receives the same additional instruction to extract only the explicitly named target task. All twelve held-out notes appear in each request. Three repetitions per arm produce nine model calls, with arm order rotated as in the first pilot.

This asks whether the variants separate on more conversational inputs. It does not isolate a single language feature or compare a representative sample of all meeting notes.

## Result

| Arm | Repetition 1 | Repetition 2 | Repetition 3 | Pooled case observations |
|---|---:|---:|---:|---:|
| short | 12/12 | 12/12 | 12/12 | 36/36 |
| rules | 12/12 | 12/12 | 12/12 | 36/36 |
| examples | 12/12 | 12/12 | 12/12 | 36/36 |

All nine responses met the strict JSON contract. Every category scored 6/6 observations per arm. Both paired comparisons had zero improvements, zero regressions, and 36 observations passing in both arms. [Complete scores and per-case results](results/pilot-2026-10-19/scores.json).

This is another ceiling result. More conversational wording did not make this small task set discriminative for the tested model. It does not establish that the prompts are equivalent or that more examples never help. The 36 observations per arm are three correlated batches, not 36 independent calls.

The recorded runtime was Codex CLI 0.163.0, gpt-6.1-sol, reasoning effort low. The [manifest](results/pilot-2026-10-19/manifest.json) retains all commands, statuses, and durations. No failed execution or model answer was omitted. Runtime duration is descriptive and billing was not measured.

## Inspect the harder cases

In n03, an existing owner proposes a conditional handover that never occurs. The original owner and deadline remain. In n05, a nearby task has a different owner and date; the target task keeps its own commitments. In n09, “tomorrow” crosses a month boundary from April 30 to May 1 using an explicit date anchor. In n11, two equally current sources disagree about ownership; the label remains null because no precedence is established.

These cases expose decisions the rubric must define. A fluent interpretation is not enough if the labeler and evaluator disagree about what counts as a commitment. That is why the next step is independent annotation and broader task coverage, rather than generating increasingly elaborate variants of the same easy test.

## Human review is a separate gate

The [review packet](review/blank.json) contains notes and blank labels. All twelve cases are marked `unreviewed`. The [review tool](review/review.py) separates unreviewed rows, uncertainty, agreements, and disagreements. Even a matching submission only becomes eligible for maintainer review; it is never automatically certified as independent human approval.

The packet omits gold answers, but the public repository cannot guarantee reviewer blindness. Reviewer identity and independence are self-declared and need maintainer confirmation. Model-generated reviews must be identified as model reviews.

## Recheck or rerun

Offline checks need no model account:

```bash
python3 labs/natural-notes/check_saved.py
python3 -m unittest discover -s labs/natural-notes/review -p 'test_*.py'
python3 labs/natural-notes/review/review.py labs/natural-notes/review/blank.json
```

A new model run consumes your Codex account usage and requires a new output directory:

```bash
python3 labs/natural-notes/run.py --output /tmp/natural-notes-new-run
```

The shared runner is snapshotted with the [recording](results/pilot-2026-10-19), alongside frozen prompts, dataset, and protocol. Future corrections need a new version and retained disagreement record. The original pilot and its tie remain unchanged.
