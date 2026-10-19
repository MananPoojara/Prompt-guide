# When is the core guide ready for maintenance?

[Roadmap](ROADMAP.md) · [Updates policy](updates/README.md)

“Everything about prompting” is not a stable finish line. The maintenance milestone is a coherent path through the decisions a reader must make, with inspectable examples and clear limits. New products and research can still add topics later.

The audit below was performed on 2026-10-19. **Initial** means a local explanation and small demonstration exist; **open** means the requirement has not been met. A topic is not complete merely because it appears in a table.

| Reader decision | Current local coverage | Remaining core work |
|---|---|---|
| How do I ask for a useful result? | First example, templates, three everyday cases | A complete planning example; ambiguity and clarification examples |
| What happens to my input? | Tokens/sampling plus embeddings/attention recordings | Connect the two visuals; explain context limits and truncation with a checked example |
| Which prompt technique should I try? | Original prompts, two controlled extraction pilots, and bounded output repair | Example order/selection and decomposition comparisons |
| How do I supply relevant evidence? | Five evidence conditions plus lexical/embedding retrieval on ten developer docs | Broader real-document evaluation, equal-context-budget comparisons, and answer generation |
| How should memory work? | Context/memory chapter and handoff explanation | Executed write/retrieve/update example with stale-memory handling |
| When should tools or an agent be used? | Local MCP connection, resumed agent, and two controlled-failure traces | Comparable single-call/workflow/agent tasks and proposed-action approval demonstrations |
| How do skills and plugins change behavior? | Public artifacts and source-inspected shortlist | An executed local skill/plugin comparison with a compatible host |
| How do I handle untrusted material? | Quoted-instruction explanation and one injection case | Broader attack/failure cases and explicit host-side boundaries |
| How do I assess changes? | Saved-output regression checks and descriptive duration reports | Independent task review, uncertainty worked example, judge calibration; actual cost accounting if billed runs are compared |
| Can a newcomer follow the guide? | Reading paths, glossary, text alternatives, mobile-tested visuals | Independent beginner and advanced reader feedback; accessibility review beyond automated checks |
| How does the guide stay current? | Daily five-repository collector and one reviewed finding | Broader primary-source coverage and a demonstrated repeatable weekly editorial pass |

## Order of work

1. Make the model explanation concrete: embeddings, attention, and context limits.
2. Improve the evidence path: retrieval, chunking, memory, and source-grounded research.
3. Compare prompting techniques and execution strategies on tasks that can expose weaknesses.
4. Expand failure handling and evaluation, preserving original outputs and failed attempts.
5. Audit the full reading path and publication process; integrate independent reader/reviewer evidence when available.

For each delivery: write the question and success/failure criteria first, save the actual execution, run applicable checks, update the local explanation, and add a dated update. Keep the main README as navigation.

## Maintenance gate

Before calling the core ready for weekly maintenance, each row needs a self-contained explanation, a complete example, an inspectable check, and accurate prerequisites. Remaining gaps must be either resolved or explicitly excluded with a reason. Independent human review cannot be supplied by another model or inferred from repository stars. No such review has been completed yet.

Weekly maintenance then means collecting changes, assessing their impact, verifying affected examples, updating the actual guide, and publishing the evidence. The daily collector supports the collection step only. It does not continuously research, verify, or write the guide on its own.
