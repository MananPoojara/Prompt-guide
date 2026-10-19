# From a first prompt to reliable systems

[Start reading](START-HERE.md) · [Back to README](README.md)

The destination is practical judgment: identify what a task needs, choose an appropriate intervention, and measure whether it helped. Knowing many prompt phrases or installing many tools does not establish that ability.

This roadmap separates material you can read now from work still needed. **Available** means explained here. **Demonstrated** means a small saved execution exists. Neither means broad reliability has been established.

## 1. Write a request someone can check

**Available:** [first complete example](handbook/01-first-example.md), [authored templates](prompts/README.md).

Understand task, evidence, constraints, examples, missing values, and output shape. Follow how a proposed date differs from a confirmed deadline. See the complete inputs and expected answer.

**Demonstrated:** [shorter versus longer extraction prompts](labs/prompt-contract/README.md). Both succeeded in one trial each; this does not show an accuracy improvement.

**Practical judgment:** explain what counts as a correct answer before comparing prompt versions.

## 2. Understand what changes when you prompt

**Available:** [model and context explanation](handbook/02-model-and-context.md), including a conceptual visual of input, tokenization, generation, and checking.

Distinguish training from inference, supplied context from learned parameters, and a generated explanation from evidence. A prompt changes the input used during inference; it does not directly rewrite the model's learned parameters.

**Still needed for deeper ML coverage:** executable tokenization examples; controlled demonstrations of sampling and output variability; explanations of embeddings, attention, and decoding grounded in inspectable small-model behavior. Illustrative diagrams must remain distinct from measurements of proprietary models.

**Practical judgment:** distinguish missing evidence, ambiguity, model error, and application error rather than blaming every failure on wording.

## 3. Design context and choose a prompting method

**Available:** [context, retrieval, memory, and handoffs](handbook/04-context-and-memory.md), [annotated public prompts](handbook/03-original-prompts.md).

Follow how evidence enters a request and how summaries preserve or lose state. Inspect published prompts with their runtime dependencies.

**Demonstrated:** a [three-arm prompt comparison](labs/prompt-comparison/README.md) with a frozen dataset and three repetitions per arm. All variants tied; the authored synthetic pilot has no independent label review.

**Still needed:** broader comparisons of zero-shot and few-shot requests; example selection and ordering; decomposition; structured-output validation and repair; retrieval failures; contradictory evidence; and prompt-injection cases with explicit trust boundaries.

**Practical judgment:** choose whether to change instructions, add examples, retrieve evidence, or fix the surrounding software.

## 4. Build a bounded agent workflow

**Available:** [skills and plugins](handbook/05-skills-and-plugins.md), [MCP](handbook/06-tools-and-mcp.md), [harnesses and graphs](handbook/07-harnesses-and-loops.md), and [external tools to try](toolkit/README.md).

**Demonstrated:** a [real local MCP connection](examples/mcp-notes/README.md), a [saved coding change](labs/search-fix/README.md), and an [evaluator/repair sequence](cases/evaluator-loop/README.md).

**Still needed:** a complete model-driven tool loop with retained traces; invalid-call and timeout recovery; permission enforcement; checkpoint/resume; and measured comparisons of a single call, a fixed workflow, and an agent loop. The sample plugin currently has static validation only.

**Practical judgment:** explain which decisions the model makes, which rules the runtime enforces, and why the process stops.

## 5. Evaluate like an engineer

**Available:** [evaluation and failure diagnosis](handbook/09-evaluation-and-failures.md), with raw outputs and small independent checks in the cases. The [controlled extraction pilot](labs/prompt-comparison/RESULTS.md) adds repeated trials, category reporting, paired comparisons, duration observations, and a documented ceiling result.

**Still needed:** independently written held-out tasks, repeated trials, paired comparisons, uncertainty estimates, error categories, judge calibration against human review, and cost/latency measurement. Model and prompt revisions need regression tracking.

**Practical judgment:** distinguish “worked once,” “improved on this evaluation,” and “reliable enough for this use.” An evaluator saying PASS is one observation, not a universal correctness proof.

## Advanced work: the next additions

These are planned additions, not completed chapters or results. Their order keeps claims dependent on evidence that actually exists.

| Priority | Addition | Evidence required before calling it demonstrated |
|---|---|---|
| 1 | Controlled prompting comparisons — [first pilot available](labs/prompt-comparison/README.md) | Add independent label review and more varied held-out cases; retain the pilot’s tie and setup failure |
| 2 | Visual ML mechanics | Runnable tokenizer and sampling examples with model/version details; conceptual graphics explicitly labeled |
| 3 | Context and retrieval experiments | Known relevant documents, retrieval logs, answer checks, missing/conflicting/adversarial evidence cases |
| 4 | Complete agent execution | Model requests, tool calls, permission decisions, failures, budgets, and recovery traces |
| 5 | Evaluation and deployment decisions | Judge agreement checks, uncertainty, cost/latency, regression results, and evidence for choosing prompting, retrieval, or fine-tuning |

A useful addition connects **a question → a technique → an observable run → a check → its limits**. More pages or more links alone do not fill these gaps.

## How to use the roadmap

Start at the first unfamiliar stage. Read a complete example and inspect its evidence. Move deeper when you can explain the failure being addressed and what would count as improvement. There are no homework requirements or claims of certification here; the goal is a resource you can revisit while doing real work.

For a specific need, jump directly to the relevant stage. For an unfamiliar term, use the [glossary](handbook/glossary.md). To add evidence for a missing topic, follow [contributing](CONTRIBUTING.md).
