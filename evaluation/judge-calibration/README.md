# Check the judge before trusting its scores

[Evaluation](../README.md) · [Human annotation packet](../../labs/natural-notes/review/README.md) · [Uncertainty lab](../../labs/eval-uncertainty/README.md)

**Status: comparison software and a synthetic worked example are available. No model judge has been calibrated against independent human review here.** The example labels and judge verdicts are deliberately authored numbers, not human feedback or model observations.

A judge can accept an incorrect answer, reject a correct one, or decline to decide. Reporting only agreement on the cases it decided hides those differences. This tool produces a separate table for calibration and test cases, preserves disagreement IDs, and shows the denominators behind every ratio.

## Work through the example

From the repository root (the directory containing `START-HERE.md`), with Python 3.10+:

```bash
python3 evaluation/judge-calibration/compare.py evaluation/judge-calibration/example.json
python3 evaluation/judge-calibration/check_example.py
python3 -m unittest discover -s evaluation/judge-calibration -p 'test_*.py'
```

No account, package installation, network request, or inference is needed. Inspect the complete [input](example.json) and [saved report](example-report.json).

The synthetic **test** split contains six rows. Two reference labels are uncertain or unreviewed; they are excluded from agreement, while reference coverage remains visible as **4/6**. The four usable reference labels give this table:

| Synthetic reference | Judge pass | Judge fail | Judge abstain | Judge missing |
|---|---:|---:|---:|---:|
| Pass | 1 | 1 | 0 | 0 |
| Fail | 1 | 0 | 1 | 0 |

The judge decides three of those four cases: **decision coverage = 3/4**. Only one decided verdict agrees: **agreement on decided cases = 1/3**. The report lists one false acceptance, one false rejection, and one abstention. The abstention is neither an agreement nor an incorrect substantive verdict; it is a case the judge did not resolve.

The synthetic **calibration** split has three usable references, two correct verdicts, and one missing judge output. Its agreement on decided cases is **2/2**, while decision coverage is **2/3**. A missing output may represent a failed or unexecuted judge call; it must not be silently relabeled as an intentional abstention. When a denominator is zero, the report returns `null`, not invented zero or perfect agreement.

These fractions illustrate bookkeeping only. They are not estimates of any real judge's performance.

## What the fields mean

| Field | Meaning |
|---|---|
| `id` | Unique candidate-response case identifier |
| `group` | Related question/document/task family that must stay in one split |
| `split` | `calibration` for developing the judge; `test` for a frozen later assessment |
| `reference` | `pass`, `fail`, `uncertain`, or `unreviewed` under a declared human-review rubric |
| `judge` | `pass`, `fail`, deliberate `abstain`, or `missing` when no valid verdict is available |

For a real submission, use `evidence_type: submitted_comparison`, declare reference type and reviewer identifier, and retain honest independence metadata. A model reference must use `type: model`; it does not become human review because it agrees with a published key. A model judge requires its requested model and exact prompt revision. Keep full instructions, candidate answers, source evidence, raw judge outputs, execution failures, and any human adjudication alongside the packet. This compact table alone is not sufficient provenance.

The tool rejects duplicate case IDs, unknown labels, invalid provenance fields, and a declared group appearing in both splits. It cannot detect undisclosed related cases, prior test exposure, dishonest reviewer metadata, or unrecorded prompt tuning. Metadata is self-reported, not identity verification. It never sets `independent_review_verified` or `calibration_certified` to true.

## A real calibration procedure

1. **Define the decision and error costs.** Write a task-specific rubric, examples of unacceptable answers, what counts as supported evidence, and when the judge should abstain. Set acceptable false-acceptance, false-rejection, and coverage targets before examining test outcomes. There is no universal passing percentage.
2. **Obtain reviewed reference decisions.** Have people assess actual candidate answers against the task and evidence. Preserve disagreements and mark unresolved cases uncertain. The existing twelve-note packet reviews extraction labels; it does not automatically supply pass/fail judgments for every candidate response. Do not turn a model's assessment into human evidence.
3. **Develop on calibration cases only.** Freeze related-case groups, adjust instructions on calibration disagreements, and retain each judge revision. Already inspected repository outputs can help development; calling them a new held-out test does not erase that exposure.
4. **Freeze and evaluate a separate test set.** Keep the judge prompt, model/settings, rubric, data, and thresholds fixed. Retain all calls, including malformed responses and failures. Encode the absence of a valid verdict as `missing`, not an invented decision. Evaluate coverage and error types together; account for related cases when estimating uncertainty.
5. **Record the disposition.** Inspect false acceptances, false rejections, abstentions, and unavailable references. State whether the predeclared targets were met for that task and whether human escalation is needed. Tuning after seeing test outcomes requires a new assessment set; preserve the original result.

To compare a completed packet and preserve a new report:

```bash
python3 evaluation/judge-calibration/compare.py /path/to/reviewed-packet.json --output /tmp/judge-comparison.json
```

The command refuses an existing output file. It performs comparison, not annotation or model inference. It does not automatically approve a judge, update the guide's human-review gate, or authorize any production decision.

## What remains open

Independent reference review, actual judge inference, a frozen calibration/test study, representative task coverage, and a justified operational threshold remain unfinished. The eight unit tests exercise the comparison and rejection logic; they do not establish judge quality. The observed capstone [wording false negatives](../../labs/capstone/RESULTS.md) explain why evaluator inspection matters, but are not a substitute for this independent study.
