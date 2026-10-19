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

The command verifies source artifacts and links, recorded model mechanics, both extraction pilots, evidence-grounding scores, and the agent trace. It fails if any constituent check fails. Repository CI additionally runs unit tests and the separate MCP integration example. See the [recorded report](report-2026-10-19.json) for actual outcomes and command output.

## Runtime and usage

The report extracts process-call durations directly from frozen manifests. It reports call counts, process successes, summed durations, and medians separately for each experiment. These are descriptive observations from sequential local runs, including CLI/service overhead. Agent pauses are excluded. They are not a model speed benchmark or an estimate of user-facing production latency.

Dollar cost is `null`: billing records were not collected. CLI usage counters are not assumed to be invoices. Before a paid comparison, declare the model, accounting method, input/output/cache token categories, price date, call budget, and treatment of failures. Never infer a zero cost from missing billing data.

## What would justify a stronger claim?

The natural-note pilot has a [human review packet](../labs/natural-notes/review/blank.json). Independent review remains pending. A model grading another model does not fill that gap. Once reviewed labels exist, compare judge decisions with human decisions, retain the disagreement table and failure types, and evaluate on separate calibration and test sets.

The repeated questions share prompts and calls, so treating each answer as an independent sample would overstate precision. We report observed counts rather than attach a misleading confidence interval. A future comparison should predeclare the unit of analysis and use paired tasks across conditions; resample at the independent task/cluster level where appropriate.

For a model or prompt revision, preserve this baseline, run a new frozen experiment, and compare task-level failures, abstentions, resolution, durations, and accounted usage. Regrading old outputs is a software regression check, not a fresh model evaluation.

## Choose the intervention that addresses the failure

| Observed problem | First intervention to investigate | Required check |
|---|---|---|
| Ambiguous request or output contract | Clearer instructions/examples | Same held-out tasks, unchanged rubric |
| Missing or stale facts | Better evidence selection and provenance | Retrieval coverage plus answer resolution |
| Invalid actions or runaway loop | Host validation, budget, and recovery | Fault tests and retained execution trace |
| Persistent behavior gap despite adequate context | Evaluate training/adaptation feasibility | Independent dataset, cost baseline, and held-out comparison |

The grounding pilot demonstrates why changing evidence can matter even when all conditions receive a perfect correctness score: correct abstention resolves fewer questions. The agent pilot demonstrates a bounded execution, not a reason every task should become an agent. No fine-tuning experiment or production deployment has been performed here.
