# Advanced practicum: diagnose, change, measure

[Lab index](README.md) · [Start with the foundations](../START-HERE.md) · [Capstone](CAPSTONE.md)

Use this path when you can already write a task, supply context, and specify an output. You need basic Python, JSON, and command-line familiarity. Run commands from the repository root. Start with Python 3.10+ and the saved artifacts; model downloads, native hosts, and authenticated inference are separate requirements in each lab.

These are **learner exercises**, not additional recorded experimental results. Predict the outcome before running a change. Keep your results in a new directory; never overwrite the published baseline or its frozen source.

## 1. Find the failure before editing the prompt

Open the [retrieval lab](retrieval/README.md) and inspect the same question under two chunk sizes:

```bash
python3 labs/retrieval/view_results.py --condition dense-48 --question double-write
python3 labs/retrieval/view_results.py --condition dense-128 --question double-write
```

Write down the highest-ranked document, the selected character spans, and the instruction the answer generator would need. Explain how a correct document can rank first while the complete reference instruction is missing.

**Deliver:** a short diagnosis with source offsets. Distinguish document relevance, complete evidence coverage, and answer correctness. Passing the first two does not measure the third.

**Extend:** add a paraphrased question without changing the document. Freeze it before running retrieval. Check whether the result survives the wording change. Do not call a single successful paraphrase a robustness benchmark.

## 2. Trace the exact request the model receives

Follow [context packing](context-budget/README.md). Inspect the saved full, prefix, suffix, and packed requests. Predict which required segment each method loses before reading the presence checks.

**Deliver:** a diagram from source files to selected text to tokenized input. Mark where instruction, evidence, and question enter the request and where each can be dropped.

**Extend:** in a separate experiment, place a relevant document after an oversized irrelevant document. Test whole-document skipping and required-segment failure. Use the documented tokenizer environment for new token measurements. Report actual assembled-string counts; do not equate this teaching tokenizer with a hosted chat API's accounting.

## 3. Separate formatting from truth

Inspect [output repair](output-repair/README.md). Compare malformed JSON, valid JSON with an invented value, and missing evidence.

**Deliver:** three separate judgments for each case: parses, satisfies the schema, supported by evidence. Identify which checks require the source rather than just the output string.

**Extend:** add a valid-looking answer with an incorrect citation. Write the expected rejection before changing the validator. The correct response to absent evidence can be an unresolved result; forcing a value makes the system less reliable.

## 4. Break the host, not just the wording

Inspect [agent recovery](agent-recovery/README.md), [memory lifecycle](memory-lifecycle/README.md), and [action approval](action-approval/README.md).

```bash
python3 -m unittest discover -s labs/agent-recovery -p 'test_*.py'
python3 -m unittest discover -s labs/memory-lifecycle -p 'test_*.py'
python3 -m unittest discover -s labs/action-approval -p 'test_*.py'
```

**Deliver:** a sequence diagram for a temporary read failure and a permission denial. Identify the host checks that prevent retries from bypassing a denial. Then explain why an expired correction must not silently resurrect the older value, and why changing an approved proposal invalidates that approval.

**Extend:** design a crash between an action and its completion record. Explain what the current in-process demo cannot guarantee. Do not claim exactly-once execution without a durable, tested recovery design.

## 5. Decide whether autonomy helps

Read [the workflow comparison](workflow-comparison/README.md). All three strategies answered these small tasks equally well, with different call counts.

**Deliver:** a decision memo choosing single call, deterministic workflow, or agent for one concrete task. Include the information available at the start, which next steps depend on intermediate results, and a failure that would change your choice.

**Extend:** predeclare a new task where the fixed selection rule is insufficient. Keep the answer rubric and task evidence shared across strategies. Count failed calls and repeated history as well as successful answers. A task invented after seeing the results is exploratory; label it that way.

## 6. Inspect a skill as an execution event

Open [native skill execution](skill-execution/README.md). Locate discovery metadata, the `Skill` invocation, its matching receipt, the document reads, and the final response.

**Deliver:** distinguish “installed,” “discovered,” “invoked,” and “helped.” Say which are supported by the recording. The presence of a skill in the prompt or a polished answer alone does not prove invocation or improvement.

**Extend:** propose a repeated comparison with equivalent host context and a predeclared task rubric. Retain unsuccessful invocation attempts. Other enabled host components are possible confounders, not details to omit.

## 7. Audit your own conclusion

Run the saved-artifact gate:

```bash
python3 evaluation/check.py --output /tmp/prompt-guide-evaluation.json
```

Then inspect [uncertainty](eval-uncertainty/README.md). Explain why repeating the same ten questions does not produce one hundred independent tasks, and why a zero-width interval on identical pairs does not prove equivalence.

**Deliver:** one claim your evidence supports, one it does not support, and the next measurement that would distinguish your explanation from an alternative. A green artifact gate verifies historical evidence; it does not execute a fresh model comparison.

Continue with the [capstone specification](CAPSTONE.md) when you can explain each boundary without relying on a model to grade its own answer.
