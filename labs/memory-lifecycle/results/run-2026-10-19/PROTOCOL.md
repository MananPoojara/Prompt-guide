# Memory lifecycle execution — 2026-10-19

Execute a deterministic SQLite application scenario on a fresh database. Fictional dates are query inputs, not claims about actual wall-clock events. Store Room A, retrieve it, correct to Room B with an earlier expiry, reject an update based on the stale revision, demonstrate namespace isolation, close/reopen the database, observe expiry without resurrecting A, then retract the fact. Preserve the full event history and the context packet produced by the host.

Use explicit source IDs, append-only API writes, optimistic revision checks inside an immediate transaction, and parameterized SQL. Expiry is exclusive: on the expiry date the value is no longer current. As-of selection finds the latest observed revision first and only then checks expiry/retraction. The application chooses the namespace; this demo does not implement caller authentication or database-file access control.

No model call is performed. The context packet is an actual deterministic application output, not a generated model response. It labels retrieved content as data, but this alone cannot prevent prompt injection. Retraction suppresses future retrieval while retaining history; it is not privacy deletion. Save code/protocol hashes and reproduce the JSON transcript against a fresh database in CI.
