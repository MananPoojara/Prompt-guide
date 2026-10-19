# 9. Evaluate a result and diagnose the failure

Previous: [Coding and verification](08-coding-and-verification.md) · [Glossary](glossary.md) · [Start](../START-HERE.md)

Evaluation means deciding how well a system satisfies a defined task using inspectable evidence. A polished answer is an observation; whether it is useful or correct depends on the criteria. Define those criteria before selecting the answer you prefer.

## Use the checker that matches the claim

For the meeting-note task, a checker can compare structured fields with an expected answer. For the search function, tests can execute the code. For a research summary, reviewers may need to compare claims with cited passages. For visual design, human judgments may be necessary, with clearly stated criteria and multiple examples.

A model evaluator can help apply a rubric or find issues, but it can also miss defects, prefer a particular writing style, or be influenced by the candidate answer. Preserve its raw verdict and distinguish it from independent program checks or human review.

The [stack case](../cases/evaluator-loop/README.md) makes this distinction concrete. The evaluator returned PASS for the comparison fixture while discussing an ambiguity about amortized versus strict constant time. A neat PASS/FAIL field does not remove ambiguity from the task specification.

## Compare systems without quietly changing the question

Suppose you want to know whether explicit missing-value rules improve note extraction. Keep the input set, model, settings, available tools, output parser, and scoring rule stable while comparing prompt versions. Record failures as well as successes. If you change several components at once, report the comparison as a system change rather than attributing everything to prompt wording.

Use examples that reflect the intended task: missing owners, proposed dates, changed dates, conflicting notes, and ordinary straightforward cases. Avoid constructing only the examples that favor your new rule. Keep some examples separate from prompt development so the comparison is less likely to reward memorizing the development set.

Repeated trials help reveal variability. More repetitions of one easy example still do not establish broad coverage. A useful report states both how many distinct inputs were used and how many trials were run per input.

The [saved comparison](../labs/prompt-contract/RESULTS.md) has four task records in one response per prompt. Both versions succeeded. That result is useful precisely because it prevents us from telling an unsupported improvement story.

## Locate the broken layer

| Symptom | Evidence to inspect first | Likely next action |
|---|---|---|
| The answer ignores a file | Actual assembled input and file-read result | Supply or retrieve the relevant file |
| A proposal becomes a commitment | Source note and interpretation rule | Clarify the decision rule; add ambiguous examples |
| A tool call has missing fields | Advertised schema and requested arguments | Repair argument construction or validation |
| A valid tool call returns no record | Lookup/search result and query | Check identifiers, retrieval, permissions, or missing data |
| The answer is correct but import fails | Raw output and parser error | Align output format and parser expectations |
| The agent says tests passed without a log | Tool execution records and exit status | Run the check and retain its actual result |
| The loop keeps revising forever | Verdicts, stop conditions, and budgets | Define acceptance and enforce termination |
| A later session forgets a decision | Saved record and actual retrieval/load trace | Repair loading or handoff, not just saving |
| The cited source does not support a claim | The source passage itself | Remove, narrow, or replace the claim |

These are starting hypotheses, not automatic diagnoses. For example, a file may have been loaded and still misunderstood. The purpose of logging is to distinguish those possibilities.

## Keep a useful failure record

A failure report needs enough information for someone else to reconstruct the observation: task, input, prompt version, runtime/model, relevant settings, available tools, raw output, expected behavior, actual check, and result. Keep secrets out of shared artifacts. If a dependency or model changes, record that change rather than replacing the old run invisibly.

Our [MCP result](../examples/mcp-notes/recorded-output.json) records SDK and negotiated protocol versions because those affect compatibility. Our [originals manifest](../originals/manifest.json) records commit hashes because upstream files can change. Our model cases preserve assembled inputs because a short user sentence does not describe the whole request.

## Decide what to change next

Choose the smallest change that addresses the observed cause. If the parser expects JSON and the model wraps it in commentary, an output constraint or structured-output interface may be appropriate. If the source data is stale, a stricter writing prompt will not refresh it. If the test suite omits duplicate minima, add that behavioral check rather than merely asking the reviewer to be more careful.

Then rerun the relevant evaluation and preserve the comparison. If performance improves only on one narrow category, say so. If the result ties, keep it. If a change improves correctness but doubles latency, report both when latency matters to users.

The goal is a resource where readers can trace a claim to an input, an output, and a check. That lets them learn a technique and also understand when it fails.
