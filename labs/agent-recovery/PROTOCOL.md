# Agent response to controlled faults — 2026-10-19

Two runs on the same fictional library corpus and questions as bounded-agent. Predeclare conditions: transient (first valid read returns a retryable error, later reads work) and denied (all valid reads return a permanent permission denial). These are deliberately injected host faults, not observed infrastructure outages. The model's subsequent decisions are live observations.

Each condition allows six fresh gpt-6.1-sol low-reasoning calls maximum, 180 seconds per call. Reserve budget before invocation, retain every exact request, response, log, tool decision/result, and checkpoint. No extra call after budget exhaustion; no retry of a failed model CLI call. Tool errors remain visible to the next model call. Documents are read-only and whitelisted; no external side effects are permitted through the dispatcher.

Expected reference behavior: transient recovers current-plan evidence and answers all three questions; denied returns insufficient_evidence with no citations for all three. Compare exact grounding judgments after the run, but retain any failures without adjusting the prompt or replacing runs. A successful trace does not establish robustness across prompts, models, or attacks. This is application JSON action dispatch, not a native tool-call API. No claim that an agent instruction alone enforces security.
