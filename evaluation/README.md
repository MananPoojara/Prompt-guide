# Know what passed before trusting the result

[Roadmap](../ROADMAP.md) · [Failure diagnosis](../handbook/09-evaluation-and-failures.md)

A successful process, a valid response, and a correct answer are different measurements. This repository retains all three where available. It does not combine unrelated tasks into a single “AI accuracy” score.

| Gate | What it establishes | What it cannot establish |
|---|---|---|
| Process status | The model CLI completed | Answer correctness |
| Schema and tool validation | Output fits the allowed interface | Claims match evidence |
| Citation provenance | Cited documents were available/read | Cited claims are true |
| Reference-answer checks | Answer matches the authored rubric | Rubric is independent or representative |
| Saved-evidence regression | Historical artifacts still pass their checks | A new model run would behave identically |

## Run the offline gate

Python 3.10+; no model account or network required:

```bash
python3 evaluation/check.py --output /tmp/prompt-guide-evaluation.json
```

The command runs 24 checks covering local links, original source artifacts, everyday planning records, model-mechanics recordings, prompt comparisons, retrieval and answers, both capstone stages, the synthetic judge-comparison example, repair, memory, agent/approval boundaries, uncertainty, and native skill execution. It fails if any constituent check fails. Repository CI additionally runs unit tests and the separate MCP integration example. See the [current artifact-check report](report-2026-10-19-judge-tools.json) for the 24-check execution. It includes synthetic examples and is not a model-judge calibration result. The [integrated-update report](report-2026-10-19-update.json) preserves its preceding 23-check execution. The [read-only capstone report](report-2026-10-19-capstone.json) preserves its preceding 22-check execution. The [earlier audit](report-2026-10-19-audit.json) preserves the preceding 21-check execution. The [initial report](report-2026-10-19.json) remains preserved as historical evidence. The new report records its base commit, whether the worktree was modified, and exact checker hashes; it does not pretend that an in-progress worktree was a clean release.

## Runtime and usage

The report extracts process-call durations from three selected historical manifests: natural notes, evidence grounding, and the bounded agent. It is not an aggregate of every lab in the repo. Newer labs retain their own durations and usage limits alongside their results. It reports call counts, process successes, summed durations, and medians separately for each experiment. These are descriptive observations from sequential local runs, including CLI/service overhead. Agent pauses are excluded. They are not a model speed benchmark or an estimate of user-facing production latency.

Dollar cost is `null`: billing records were not collected. CLI usage counters are not assumed to be invoices. Before a paid comparison, declare the model, accounting method, input/output/cache token categories, price date, call budget, and treatment of failures. Never infer a zero cost from missing billing data.

## What would justify a stronger claim?

The natural-note pilot has a [human review packet](../labs/natural-notes/review/blank.json). Independent review remains pending. The [reader feedback packet](../review/README.md) separately addresses usability. A model grading another model does not fill either gap. The [judge-comparison tool and worked example](judge-calibration/README.md) now show the bookkeeping and split checks. Its inputs are synthetic, and it does not satisfy the human-review or calibration gate. Once reviewed labels exist, compare actual judge decisions with human decisions and retain disagreements on separate calibration and test sets.

The repeated questions share prompts and calls, so treating each answer as an independent sample would overstate precision. We report observed counts rather than attach a misleading confidence interval. A future comparison should predeclare the unit of analysis and use paired tasks across conditions; resample at the independent task/cluster level where appropriate. The [uncertainty worked example](../labs/eval-uncertainty/README.md) demonstrates paired cluster resampling and hypothetical Wilson intervals while making the authored-data assumptions explicit.

For a model or prompt revision, preserve this baseline, run a new frozen experiment, and compare task-level failures, abstentions, resolution, durations, and accounted usage. Regrading old outputs is a software regression check, not a fresh model evaluation.

## Choose the intervention that addresses the failure

| Observed problem | First intervention to investigate | Required check |
|---|---|---|
| Ambiguous request or output contract | Clearer instructions/examples | Same held-out tasks, unchanged rubric |
| Missing or stale facts | Better evidence selection and provenance | Retrieval coverage plus answer resolution |
| Invalid actions or runaway loop | Host validation, budget, and recovery | Fault tests and retained execution trace |
| Persistent behavior gap despite adequate context | Evaluate training/adaptation feasibility | Independent dataset, cost baseline, and held-out comparison |

The grounding pilot demonstrates why changing evidence can matter even when all conditions receive a perfect correctness score: correct abstention resolves fewer questions. The agent pilot demonstrates a bounded execution, not a reason every task should become an agent. No fine-tuning experiment or production deployment has been performed here.
