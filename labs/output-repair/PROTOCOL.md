# Bounded output repair protocol — 2026-10-19

Three authored damaged-response fixtures: invalid JSON, valid JSON with unsupported commitments, and unavailable evidence. These are injected failures, not claims that a model produced those initial mistakes. Freeze fixtures, contract, prompt, and runner before execution.

For each fixture, record deterministic contract errors and reference agreement before repair. Make exactly one fresh gpt-6.1-sol low-reasoning call through Codex, with a 180-second timeout. Supply documents, candidate, and contract errors, never the expected-reference object. This is prompt-based JSON repair, not a provider-native structured-output guarantee. Retain raw request/response/log, status, duration, and exact command. No retry after model failure. Recompute contract errors and exact authored-reference agreement afterward. Both checks passing establishes success only for the fixture. Missing evidence must result in needs_review with no records.

The reference check is an offline evaluation oracle with authored labels; a production application does not automatically possess such an oracle. No writes or external actions occur. Review status is illustrative and does not enqueue a real human reviewer. Do not claim a general truth validator, calibrated repair rate, or provider comparison from three cases.
