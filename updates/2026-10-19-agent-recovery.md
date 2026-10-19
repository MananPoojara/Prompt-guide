# 2026-10-19 — Retry a temporary error; respect a denial

**For:** developers building agents around fallible tools.

The [agent-recovery lab](../labs/agent-recovery/README.md) records actual model decisions under two deliberately injected host faults. A temporary read error led to one retry, successful evidence retrieval, and three checked answers in four calls. A permanent read denial led to an insufficient-evidence final response in three calls, with no unread citations or additional read attempt.

Both conditions passed 3/3 reference checks, but the denied condition resolved zero questions. Correctly respecting missing access is distinct from completing the information task. The host enforces the denial and read receipts; the prompt alone is not the access-control boundary.

**Evidence:** seven live model calls, full request/output/tool/checkpoint traces, four fault-policy tests, and deterministic replay of both runs. The service failures were controlled injections, not real infrastructure outages. No general robustness or sandbox-security claim follows from these traces.

**Action:** classify errors before deciding to retry, consume retries from a bounded budget, and preserve a visible failure/abstention path. The developer lab index, harness chapter, and roadmap now link the extension.
