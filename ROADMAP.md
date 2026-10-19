# From a first prompt to reliable systems

[Start reading](START-HERE.md) · [Back to README](README.md)

The destination is practical judgment: identify what a task needs, choose an appropriate intervention, and measure whether it helped. Knowing many prompt phrases or installing many tools does not establish that ability.

The [core coverage audit](CORE-COVERAGE.md) defines the remaining work before moving primarily to weekly maintenance.

This roadmap separates material you can read now from work still needed. **Available** means explained here. **Demonstrated** means a small saved execution exists. Neither means broad reliability has been established.

## 1. Write a request someone can check

**Available:** [first complete example](handbook/01-first-example.md), [authored templates](prompts/README.md).

Understand task, evidence, constraints, examples, missing values, and output shape. Follow how a proposed date differs from a confirmed deadline. See the complete inputs and expected answer.

**Also available:** [five complete everyday cases](everyday/README.md), including constrained planning and a scripted clarification exchange.

**Demonstrated:** [shorter versus longer extraction prompts](labs/prompt-contract/README.md). Both succeeded in one trial each; this does not show an accuracy improvement.

**Practical judgment:** explain what counts as a correct answer before comparing prompt versions.

## 2. Understand what changes when you prompt

**Available:** [model and context explanation](handbook/02-model-and-context.md), including a conceptual visual of input, tokenization, generation, and checking.

Distinguish training from inference, supplied context from learned parameters, and a generated explanation from evidence. A prompt changes the input used during inference; it does not directly rewrite the model's learned parameters.

**Demonstrated:** the [model-mechanics lab](labs/model-mechanics/README.md) records seven tokenizations, next-token logits, and 20 greedy/sampled continuations from a pinned DistilGPT2 revision. An offline visual exposes tokens, probabilities, and saved outputs.

**Also demonstrated:** [embeddings and attention](labs/representations/README.md), with full recorded vectors, all heads, and an offline visual.

**Also demonstrated:** [context-budget handling](labs/context-budget/README.md), with exact tokenizer measurements and checks for dropped instructions, evidence, and questions.

**Still needed for deeper ML coverage:** broader model comparisons and measured learning outcomes. Illustrative diagrams must remain distinct from measurements of proprietary models.

**Practical judgment:** distinguish missing evidence, ambiguity, model error, and application error rather than blaming every failure on wording.

## 3. Design context and choose a prompting method

**Available:** [context, retrieval, memory, and handoffs](handbook/04-context-and-memory.md), [annotated public prompts](handbook/03-original-prompts.md).

Follow how evidence enters a request and how summaries preserve or lose state. Inspect published prompts with their runtime dependencies.

**Demonstrated:** a [three-arm prompt comparison](labs/prompt-comparison/README.md) with a frozen dataset and three repetitions per arm. All variants tied; the authored synthetic pilot has no independent label review.

**Also demonstrated:** the [naturalistic-note follow-up](labs/natural-notes/README.md) adds twelve dialogue/context cases and a human-review packet. It also tied; independent annotation remains pending.

**Demonstrated for context:** the [evidence-availability lab](labs/evidence-grounding/README.md) retains ten calls across missing, stale, current, conflicting, and injected evidence conditions. It separates appropriate abstention from question resolution.

**Also demonstrated:** [developer-document retrieval](labs/retrieval/README.md) compares BM25 and MiniLM on two chunk sizes plus a truncated-document baseline, retaining every vector and rank.

**Also demonstrated:** [real-document retrieval and answer generation](labs/real-docs/README.md), with a shared evidence ceiling and twelve recorded answer calls on a pinned official specification corpus.

**Also demonstrated:** [bounded output repair](labs/output-repair/README.md) separates schema acceptance from reference correctness and missing-evidence review.

**Also demonstrated:** an [executed memory lifecycle](labs/memory-lifecycle/README.md), including durable corrections, expired values, and a generated context packet.

**Also demonstrated:** [example selection, ordering, and two-stage decomposition](labs/example-design/README.md), with a frozen five-condition comparison.

**Still needed:** broader task difficulty, independent labels, and realistic adversarial evaluation beyond authored corpora.

**Practical judgment:** choose whether to change instructions, add examples, retrieve evidence, or fix the surrounding software.

## 4. Build a bounded agent workflow

**Available:** [skills and plugins](handbook/05-skills-and-plugins.md), [MCP](handbook/06-tools-and-mcp.md), [harnesses and graphs](handbook/07-harnesses-and-loops.md), and [external tools to try](toolkit/README.md).

**Demonstrated:** a [real local MCP connection](examples/mcp-notes/README.md), a [saved coding change](labs/search-fix/README.md), and an [evaluator/repair sequence](cases/evaluator-loop/README.md).

**Demonstrated:** a [bounded agent](labs/bounded-agent/README.md) chooses search/read actions, resumes a saved checkpoint, and returns checked answers. Denied calls, timeouts, and budget exhaustion have simulated tests.

**Also demonstrated:** [controlled tool failures](labs/agent-recovery/README.md), with actual model responses to a transient read error and a permission denial.

**Also demonstrated:** [twelve strategy-comparison runs](labs/workflow-comparison/README.md) and [exact-action approval mechanics](labs/action-approval/README.md), with scripted review explicitly distinguished from human authorization.

**Also demonstrated:** [untrusted-content boundaries](labs/trust-boundaries/README.md), including controlled authority/scope/action attacks and a wrong-answer negative control.

**Still needed:** adaptive adversarial and real-outage evidence, authenticated review integrations, and comparisons on more varied tasks. The sample plugin now has a [native invocation and baseline review](labs/skill-execution/README.md), with host metadata and tool receipts retained.

**Practical judgment:** explain which decisions the model makes, which rules the runtime enforces, and why the process stops.

## 5. Evaluate like an engineer

**Available:** [evaluation and failure diagnosis](handbook/09-evaluation-and-failures.md), with raw outputs and small independent checks in the cases. The [controlled extraction pilot](labs/prompt-comparison/RESULTS.md) adds repeated trials, category reporting, paired comparisons, duration observations, and a documented ceiling result.

**Available now:** an [offline regression gate and runtime report](evaluation/README.md), with explicit evidence levels and remaining review gates.

**Also available:** an [uncertainty worked example](labs/eval-uncertainty/README.md), with paired document-cluster resampling and explicit limits on interpreting authored data.

**Still needed:** independently written held-out tasks, broader repeated/paired comparisons, uncertainty estimates supported by representative study design, judge calibration against human review, and actual billing-cost measurement. Model and prompt revisions need regression tracking.

**Practical judgment:** distinguish “worked once,” “improved on this evaluation,” and “reliable enough for this use.” An evaluator saying PASS is one observation, not a universal correctness proof.

## Advanced tracks: delivered evidence and remaining review

| Track | Demonstrated here | Remaining work or explicit limit |
|---|---|---|
| Prompt comparisons | [Repeated extraction](labs/prompt-comparison/README.md), [natural notes](labs/natural-notes/README.md), [example order and decomposition](labs/example-design/README.md) | Independent labels and broader task difficulty; ties remain valid results |
| Visual ML mechanics | [Tokens and sampling](labs/model-mechanics/README.md), [representations](labs/representations/README.md), [context budgets](labs/context-budget/README.md) | Small open-model measurements, not proprietary-model internals or a learning-outcome study |
| Context and retrieval | [Lexical/dense retrieval](labs/retrieval/README.md), [equal-budget real-document answers](labs/real-docs/README.md), [memory lifecycle](labs/memory-lifecycle/README.md) | Independent labels, broader questions, repeated generation, and production source/access controls |
| Agent execution | [Resumed loop](labs/bounded-agent/README.md), [recovery](labs/agent-recovery/README.md), [strategy comparison](labs/workflow-comparison/README.md), [approval](labs/action-approval/README.md), [trust boundaries](labs/trust-boundaries/README.md) | Local teaching hosts; authenticated production review, distributed recovery, and adaptive attack evaluation remain outside these demonstrations |
| Evaluation | [Regression gate](evaluation/README.md), [uncertainty](labs/eval-uncertainty/README.md), per-lab durations and limits | Human review and judge calibration pending; no invoices, fine-tuning comparison, or production deployment claimed |

A useful addition connects **a question → a technique → an observable run → a check → its limits**. More pages or more links alone do not fill missing evidence. The [practicum](labs/PRACTICUM.md) connects these labs; the [capstone](labs/CAPSTONE.md) now has a [read-only implementation](labs/capstone/README.md). Integrated recovery and proposed updates remain unfinished, and the authored pilot is not an independent benchmark.

## How to use the roadmap

Start at the first unfamiliar stage. Read a complete example and inspect its evidence. Move deeper when you can explain the failure being addressed and what would count as improvement. There are no homework requirements or claims of certification here; the goal is a resource you can revisit while doing real work.

For a specific need, jump directly to the relevant stage. For an unfamiliar term, use the [glossary](handbook/glossary.md). To add evidence for a missing topic, follow [contributing](CONTRIBUTING.md).

## Next development cycle

The aim is one dependable place to learn, practice, and keep up with prompting. “Best” is an ambition, not a verified ranking. We will judge progress by whether readers can complete a task, understand the explanation locally, inspect its evidence, and tell when guidance was last checked.

### Entry paths for different readers

| Reader | Starting experience | Continue with / remaining evidence |
|---|---|---|
| First-time AI user | [One complete prompt](handbook/01-first-example.md), with unfamiliar words explained | [Five everyday examples](everyday/README.md); independent beginner feedback remains open |
| Writer, student, or researcher | [Templates](prompts/README.md) and [evidence checking](handbook/09-evaluation-and-failures.md) | Complete source-grounded research and revision examples, including fabricated-claim and citation failures |
| Developer or automation builder | [Coding verification](handbook/08-coding-and-verification.md), [MCP](handbook/06-tools-and-mcp.md), and [toolkit](toolkit/README.md) | [Traced workflow and recovery](labs/bounded-agent/README.md), [host boundaries](labs/trust-boundaries/README.md); independent developer feedback remains open |
| Advanced experimenter | [Controlled comparison](labs/prompt-comparison/README.md) and its raw artifacts | [Uncertainty](labs/eval-uncertainty/README.md) and per-lab durations; independent labels, harder tasks, and invoice-backed cost comparisons remain open |

Readers can enter where their task starts. The advanced path should not make basic explanations harder to find. Translation will follow stable explanations and terminology, with language review; unreviewed machine translations will not be labeled verified.

### Prioritized milestones

These are delivery milestones, not a promise to finish one every week. A weekly update can report a partial investigation honestly.

| Order | Milestone | Deliverables | Completion evidence |
|---|---|---|---|
| 1 | Visual mechanics and everyday entry — first delivery available | [Tokenization/sampling lab](labs/model-mechanics/README.md) and [five noncoding cases](everyday/README.md) | Recorded model outputs, versions, data checks, browser checks, and author-reviewed examples; independent reader testing remains open |
| 2 | Stronger prompt experiments | More natural notes; documented annotation disagreements; frozen development/held-out split; comparisons of examples and decomposition | Independent reviewer attribution when obtained; predeclared rubric; all trials retained; category and paired error reports; uncertainty appropriate to the design |
| 3 | Context and retrieval | A local document set with known answers; retrieval logs; missing, stale, conflicting, and instruction-like evidence cases | Trace the retrieved material to the answer; compare retrieval and interpretation errors separately; preserve failed answers |
| 4 | Complete agent workflow | Evolve the notes example into document lookup, extraction, and proposed updates for review; retain a full execution trace | Explicit stop conditions, invalid-call handling, permission decisions, timeout behavior, checkpoint/resume, and independent output checks |
| 5 | Operational evaluation | Regression set; model-judge calibration; runtime and usage reporting; choosing prompting versus retrieval versus training | Disclose model/settings, billing assumptions, uncertainty, human-review procedure, and cases where an approach is unsuitable |

The first milestone now includes token boundaries and sampling on an inspectable small model. Readers can choose saved inputs/settings in the visual and use the Python recorder for arbitrary text. It must separate measured behavior from a simplified diagram; it must not imply that an attention visualization reveals a complete explanation of reasoning.

The everyday track uses examples such as revising a message for a defined audience, summarizing a supplied document without inventing details, and explaining a concept while checking understanding. Each needs the complete input, a usable request, an output with a provenance label, a check, and a failure case. A blank template alone does not satisfy this milestone.

### Updates are part of the product

The [updates index and review policy](updates/README.md) define the weekly process, with a [first completed editorial pass](updates/reviews/2026-10-19/README.md). Each meaningful update must answer: what changed, who it affects, what to do, what supports it, and which local page was revised. A source link without a practical explanation is insufficient.

Keep publication reviewed. A daily source-watch workflow now collects HEAD changes for nine toolkit and primary repositories into an Actions report. Its hosted execution is verified; ongoing weekly editorial continuity is not yet established. It does not publish advice; coverage and scheduling limits are described in the updates policy.

### Quality gates for every milestone

- **Self-contained:** include the necessary context, explanation, example, and check in the repository; cite sources for provenance.
- **Accessible:** define prerequisites, provide text alternatives to visuals, and distinguish reading-only access from account, installation, or compute requirements.
- **Reproducible:** record relevant versions, commands, inputs, raw outputs, and failure cases; check the documented path in a fresh environment when executable.
- **Honest:** identify authored illustrations, source-inspected claims, local executions, and independent review separately. Report ties and regressions.
- **Maintainable:** assign a local home for each topic, link it from the appropriate path, state actual review dates, and include a correction path.

### How we will know the resource is improving

Measure reader task completion and points of confusion through consented feedback, then report the number and type of participants. Track broken examples, reproducible runs, known stale recommendations, and corrections resolved. Use stars and visits as interest signals, not evidence that the explanations work. No independent usability study has been completed yet. The [reader review packet](review/README.md) provides concrete beginner/developer tasks and a consent-aware feedback form.

A finished milestone should reduce a specific reader's need to search elsewhere while preserving their ability to inspect primary sources. Coverage expands through tested additions, not a claim that every prompting technique or product update has been captured.
