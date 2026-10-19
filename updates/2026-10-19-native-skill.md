# 2026-10-19 — The sample plugin now has a native execution trace

**For:** developers learning what changes when a host loads and invokes a skill.

The [native skill lab](../labs/skill-execution/README.md) records a baseline review with skills disabled and a review explicitly invoking `prompt-guide:inspect-evidence`. Claude Code 2.1.303 discovered the local plugin, accepted the Skill call, and read the saved evidence. Both reviews rejected the unsupported accuracy claim; the skill response used the five requested sections.

The model alias resolved to `claude-sonnet-5-5` in both runs. Host built-ins remained present, so this is a native-loading demonstration rather than a fully isolated instruction experiment. No accuracy advantage or independent human review is claimed. CLI-reported cost estimates are retained separately from unverified billing.

**Evidence:** source hashes, unchanged evidence files, actual discovery metadata, a successful launch receipt, tool reads, final responses, five transcript-filter tests, and an offline checker. Published protocol events are explicitly filtered to omit reasoning/signature and account/session fields; final response text is unchanged. No global plugin installation occurred.

**Action:** verify runtime discovery and invocation before claiming that a skill affected a task. The sample plugin README, skills chapter, roadmap, developer path, and coverage audit now distinguish static validation from executed evidence.
