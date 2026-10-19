# Observed result: a tie

Executed 2026-10-19 using Codex CLI 0.163.0, model `gpt-6.1-sol`, provider `openai`, reasoning effort `none`, read-only sandbox, and fresh ephemeral sessions. Baseline ran first, candidate second. Neither requested external tools. Each variant had one attempt containing four cases.

| Variant | Correct records | Complete output matches rubric |
|---|---:|---|
| Baseline | 4 / 4 | Yes |
| Candidate | 4 / 4 | Yes |

Both outputs are identical after JSON parsing. The shorter prompt was sufficient for these notes. Explicit policy may still help more ambiguous inputs, but this experiment does not establish that claim.

The expected output and both prompts were written before either run. No retries were selected to improve the score. The six grader tests cover valid data, an invented owner, extra and missing records, invalid formatting, and a wrong top-level type.

## Limits

Four synthetic notes in a shared batch are not four independent model trials. One attempt per variant cannot estimate reliability. The order was not randomized. The candidate adds policy information as well as words. No held-out task set or different model was tested. No latency or monetary-cost measurements were collected. Codex's runtime instructions remain part of the experiment.

A larger trial should include contradictory notes, indirect assignments, uncertain dates, and adversarial embedded instructions, with an independently reviewed rubric. Preserve any regressions or ties rather than manufacturing a success story.
