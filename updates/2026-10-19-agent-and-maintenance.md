# 2026-10-19 — An inspectable agent and a maintenance loop

**For:** readers moving from context design into agents, and contributors checking whether an update is supported.

The [bounded-agent lab](../labs/bounded-agent/README.md) performed one three-call run: search metadata, read the approved document, then answer three questions. Execution stopped after search and resumed from its saved checkpoint. All three answers passed a separate reference check. Requests, responses, logs, tool results, and checkpoints are retained. Fault handling is covered by simulated tests, not claimed as observed live failures.

The [evaluation guide](../evaluation/README.md) adds an offline regression command and duration/accounting report. It distinguishes process success, citation provenance, content correctness, and question resolution. No billing cost, independent human annotation, judge calibration, or production-readiness claim is inferred from missing evidence.

The daily [source-watch workflow](../.github/workflows/source-watch.yml) compares five toolkit repositories with the revisions we inspected. It produces an Actions report for editorial review, without automatically changing recommendations. This is a limited recurring collector, not a continuously running research agent. Consult the [policy](README.md) for scope and schedule limits.

**Evidence:** live agent run and deterministic trace replay; simulated runtime fault tests; source-watch unit tests and actual GitHub API collection. The model, corpus, code hashes, and timing evidence are in the linked artifacts. GitHub scheduling behavior was source-inspected on this date.

**Action:** follow the trace before adding autonomy to a task; run the offline gate before changing graders. Review upstream differences before changing inspected revisions. The main roadmap now links these initial deliveries while retaining the deeper work as planned.
