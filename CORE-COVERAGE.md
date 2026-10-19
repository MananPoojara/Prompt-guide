# When is the core guide ready for maintenance?

[Roadmap](ROADMAP.md) · [Updates policy](updates/README.md)

“Everything about prompting” is not a stable finish line. The maintenance milestone is a coherent path through the decisions a reader must make, with inspectable examples and clear limits. New products and research can still add topics later.

The audit below was performed on 2026-10-19. **Initial** means a local explanation and small demonstration exist; **open** means the requirement has not been met. A topic is not complete merely because it appears in a table.

| Reader decision | Current local coverage | Remaining core work |
|---|---|---|
| How do I ask for a useful result? | First example, templates, and five everyday cases including planning and a scripted clarification exchange | Initial everyday path demonstrated; independent beginner feedback remains open |
| What happens to my input? | Linked token/sampling and representation visuals, plus measured context-budget example | Core mechanics path demonstrated; broader architectures and multimodal accounting remain extensions |
| Which prompt technique should I try? | Original prompts, extraction pilots, bounded repair, and a five-condition example/decomposition comparison | Initial technique comparisons demonstrated; broader task difficulty and independent labels remain extensions |
| How do I supply relevant evidence? | Five evidence conditions, fictional retrieval corpus, and six official specification pages with equal-budget retrieval and twelve answer calls | Initial real-document pipeline demonstrated; [read-only capstone](labs/capstone/README.md) integrates scope/current filtering, packing, and answer checks. [Recovery/update integration](labs/capstone-update/README.md) is demonstrated separately; independent evidence review remains unfinished |
| How should memory work? | Executed SQLite lifecycle, current-context packet, and handoff explanation | Local lifecycle demonstrated; source adjudication and production authorization/deletion are explicitly outside this lab |
| When should tools or an agent be used? | MCP connection, resumed/faulted agents, twelve strategy-comparison runs, and a scripted exact-action approval demo | Local comparison and [resumed update integration](labs/capstone-update/README.md) demonstrated; review is scripted, while authenticated production review and distributed actions remain outside these labs |
| How do skills and plugins change behavior? | Native Claude Code plugin discovery/invocation trace, baseline review, and source-inspected shortlist | Local host execution demonstrated; broader repeated comparisons and other hosts remain extensions |
| How do I handle untrusted material? | Five controlled attachment conditions, nine direct host probes, and a provenance-only negative control | Initial host boundaries demonstrated; adaptive/multi-turn attacks, trusted ingestion, and production authorization remain extensions |
| How do I assess changes? | Saved-output regression checks, duration reports, executable uncertainty illustration, and a [synthetic judge-comparison example](evaluation/judge-calibration/README.md) | Independent task review and judge calibration; actual cost accounting if billed runs are compared |
| Can a newcomer follow the guide? | Reading paths, glossary, text alternatives, mobile-tested visuals | Independent beginner and advanced reader feedback; accessibility review beyond automated checks |
| How does the guide stay current? | Daily nine-repository collector, scoped baselines, and a completed editorial pass with before/after reports | Initial procedure demonstrated; ongoing weekly continuity and broader website/paper monitoring remain open |

## Order of work

1. Make the model explanation concrete: embeddings, attention, and context limits.
2. Improve the evidence path: retrieval, chunking, memory, and source-grounded research.
3. Compare prompting techniques and execution strategies on tasks that can expose weaknesses.
4. Expand failure handling and evaluation, preserving original outputs and failed attempts.
5. Audit the full reading path and publication process; integrate independent reader/reviewer evidence when available.

For each delivery: write the question and success/failure criteria first, save the actual execution, run applicable checks, update the local explanation, and add a dated update. Keep the main README as navigation.

## Maintenance gate

Before calling the core ready for weekly maintenance, each row needs a self-contained explanation, a complete example, an inspectable check, and accurate prerequisites. Remaining gaps must be either resolved or explicitly excluded with a reason. Independent human review cannot be supplied by another model or inferred from repository stars. No such review has been completed yet. The [reader packet](review/README.md) is ready; an [AI-simulated walkthrough](review/simulated-reader-2026-10-19.md) identified two documentation fixes but does not satisfy this gate. The [current offline audit](evaluation/report-2026-10-19-judge-tools.json) checks saved evidence, not teaching effectiveness.

Weekly maintenance then means collecting changes, assessing their impact, verifying affected examples, updating the actual guide, and publishing the evidence. The daily collector supports the collection step only. It does not continuously research, verify, or write the guide on its own.
