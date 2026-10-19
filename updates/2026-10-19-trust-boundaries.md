# Test the host even when the model cooperates

The [untrusted-content lab](../labs/trust-boundaries/README.md) records five next-action proposals under ordinary text and four controlled attack patterns. All five model responses answered correctly. That result alone does not test whether a host would reject a hostile proposal.

Nine separately labeled authored probes exercise the host directly: cross-scope reads, extra namespace/approval arguments, unavailable outbound and memory actions, and spoofed source authority. Six forbidden proposals were denied or rejected. A deliberately wrong answer with valid provenance was accepted by the host and rejected by the separate reference check.

The [full results](../labs/trust-boundaries/RESULTS.md) distinguish observed model behavior, enforced host behavior, and factual correctness. The local fixture has no real credentials or outbound/write capability. It demonstrates boundaries, not production security or universal injection resistance.
