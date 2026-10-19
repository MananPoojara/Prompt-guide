# 2026-10-19 — Valid JSON is not a fact check

**For:** developers turning model responses into application data.

The [output-repair lab](../labs/output-repair/README.md) injects three authored faults: a trailing comma, a schema-valid invented commitment, and a response claiming unavailable evidence. Each receives one actual model repair attempt. All three final responses passed the contract and matched their authored references. The missing-evidence case returned `needs_review` with no records.

The valid-but-invented candidate passed schema and citation-ID checks before repair. That makes the distinction concrete: a real document ID does not prove that the cited document supports a value. The experiment has a separate authored reference oracle; a production application needs its own appropriate verification/review process.

**Evidence:** three retained Codex calls with exact inputs, outputs, logs, code hashes, and before/after judgments. Nine unit tests and offline replay passed. The contract module measured 94% statement coverage with Coverage 7.16.2; this does not measure factual accuracy. No provider-native constrained-output API was used.

**Action:** make downstream acceptance rules explicit, cap repair attempts, and route missing evidence to review instead of guessing. A host can detect an empty evidence set directly; the model call in that fixture is a boundary demonstration, not an efficiency recommendation. The developer lab path, roadmap, and evaluation chapter now link the lab.
