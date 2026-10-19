# Naturalistic notes pilot: predeclared protocol

Question: do the same three prompt approaches distinguish themselves when notes include dialogue, conditional commitments, nearby tasks, stale quoted material, date anchors, and unresolved conflicts?

This is a new authored synthetic dataset, not real participant notes. Eight development records are carried over from the first pilot. Twelve new held-out records cover six categories with two notes each. The prompts retain the prior task/rules/examples construction, with one identical addition to all arms: extract only the named Target task when present. Four development examples appear only in the examples arm.

The authoring assistant reviewed each gold answer and recorded its rationale. No independent human reviewer has supplied labels. A blank review packet is published with all cases initially marked unreviewed. It omits the answer key, but because the repository is public it cannot guarantee reviewer blindness. Any future disagreement must be documented before a revised dataset and new run; the current raw results remain immutable.

Use the shared runner/scorer from labs/prompt-comparison, with this directory as its source root. Freeze prompts, dataset, protocol, and the shared runner snapshot before the first call. Model gpt-6.1-sol, reasoning effort low, Codex CLI, fresh ephemeral read-only sessions, and no requested tools. Three repetitions, rotating short/rules/examples order as in the original pilot; all twelve notes appear in each request in fixed order. Nine calls total, 180-second timeout per call, no outcome-selected retries.

The JSON contract and rubric are unchanged: exact ordered IDs, owner and ISO deadline or null, no extra fields. Invalid batch schemas score zero for all cases; valid batches receive case-level exact-field checks. Date anchors must be supplied by the note. Conditional offers do not override current commitments unless the condition and reassignment are actually established.

Report all trial scores, category errors, paired improvements/regressions, schema and execution failures, and median CLI durations. Thirty-six observations per arm come from three correlated batches of twelve notes. Do not report binomial confidence intervals treating them as independent. Runtime durations are descriptive, not controlled speed comparisons. Account billing is not measured.

A perfect result is a ceiling observation, not proof of reliability. The task remains narrow, the author and evaluator designer are the same, and examples share a domain. Independent review, real-world task diversity, alternative model evaluation, and calibrated uncertainty remain open work.
