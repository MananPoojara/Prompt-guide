# 2026-10-19 — Compare autonomy, then bind approval to the exact action

**For:** developers deciding whether a task needs an agent and how to constrain a proposed write.

The [workflow comparison](../labs/workflow-comparison/README.md) executed twelve task runs across single-call, fixed-workflow, and agent strategies. Each strategy passed all twelve answer checks. The agent used four calls per task versus one for the alternatives; its routine runs performed an extra search. All 24 calls are retained. These small authored tasks fit in one request and expose clear metadata, so the result does not generalize to tasks needing adaptive actions.

The [action-approval lab](../labs/action-approval/README.md) records one actual model proposal and applies it only after a scripted fixture approves its exact digest. Unapproved and tampered proposals are rejected. The approved edit changes a disposable file and same-process replay reports already applied. Human review, production authentication, and crash-safe distributed effects are explicitly not established.

**Evidence:** frozen prompts/code/scorers, raw outputs, tool traces, before-state hashes, local file outcomes, four workflow tests, nine approval tests, and offline reconstruction. Request characters and call durations are descriptive; billing cost remains unknown. The original proposal recording is retained alongside a later duplicate-key parser hardening.

**Action:** compare an agent with the fixed alternative, preserve failed or tied results, and ensure that changing an approved proposal requires new review. The developer lab path, harness chapter, roadmap, and coverage audit now link both demonstrations.
