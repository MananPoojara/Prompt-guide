# 3. Read an original lab prompt in context

Previous: [Model and context](02-model-and-context.md) · Next: [Context and memory](04-context-and-memory.md)

An original public prompt is valuable because you can inspect a real published design choice. Its publisher, revision, intended runtime, and surrounding code matter as much as its wording. A prompt from a demonstration notebook is evidence of that demonstration, not proof of a company's universal production practice.

Our [originals directory](../originals/README.md) contains six licensed artifacts with attribution and hashes. The [manifest](../originals/manifest.json) records the exact upstream commits. The source files are local so you do not need to follow a blog link to read them.

## The Anthropic evaluator: instructions plus material to judge

Open the short [original evaluator prompt](../originals/vendor/anthropic-cookbook/evaluator_prompt.txt). It asks for a judgment about a response to a coding task. Its named concerns include correctness, time complexity, and style. It specifies XML-like fields for an evaluation and feedback.

The structure does several jobs:

| Part | Practical purpose | What still has to be supplied |
|---|---|---|
| Evaluator role | Makes the requested activity review rather than generation | The original task and candidate answer |
| Criteria | Directs attention to particular qualities | A clear task specification |
| Verdict vocabulary | Makes a downstream decision easier to parse | Code that handles invalid or missing verdicts |
| Feedback field | Gives the next generator concrete issues to address | A loop that actually passes the feedback on |

The prompt is not a complete executable. In the upstream notebook, code combines it with `Original task:` and `Content to evaluate:`. Without those inputs, the evaluator has no candidate to assess. Without loop code, its feedback does not automatically cause a revision.

Our [recorded request](../cases/evaluator-loop/results/run-2026-10-19) includes the actual assembled inputs and outputs. The implementation under review is a stack: a structure where the last value pushed is the first popped. It must also report the minimum stored value.

Consider pushing `3`, then `1`, then another `1`, and popping once. One `1` remains, so the minimum must still be `1`. The defective implementation forgets that repeated minimum and returns `3`. This is a small case where a reader can understand the failure before trusting the evaluator.

The original evaluator prompt, run through our local Codex runtime, returned FAIL for the defective fixture in three trials. The comparison fixture received PASS in three trials. The raw outputs also raised an important complexity ambiguity: Python's dynamic-array append is amortized constant time, which differs from a strict worst-case constant-time requirement.

## The generator: feedback becomes input

The companion [original generator prompt](../originals/vendor/anthropic-cookbook/generator_prompt.txt) directs generation. The surrounding workflow supplies prior attempts and evaluator feedback. This is the essential transition: review becomes useful only when the next request actually contains the information needed to fix the defect.

We passed the first recorded failure and defective code to that generator. The [full revision request](../cases/evaluator-loop/results/revision.input.txt) and [raw response](../cases/evaluator-loop/results/revision.output.txt) are local. The model generated a linked-node stack that stores the minimum at each node. Popping a node naturally restores the previous minimum, including when minima repeat.

Independent behavior checks passed. The follow-up model evaluator also returned PASS. These are two different observations: program checks establish specific behavior; a generated evaluator verdict establishes what that model said. Read the [full case](../cases/evaluator-loop/README.md) for the runtime and limits. We did not reproduce the upstream Claude environment and did not run a no-feedback control.

## Other original files have different jobs

The [OpenAI compaction prompt](../originals/vendor/openai-codex/compaction.md) asks for a continuation summary. Its job is to preserve useful working state when the conversation is condensed. It does not by itself store a file, select a model, or decide when compaction occurs. The runtime supplies those mechanics.

The [published Codex model-specific prompt](../originals/vendor/openai-codex/gpt-5.2-codex_prompt.md) is much larger. Read it as an application instruction artifact tied to its recorded revision and model context. This repository does not claim it is the current default prompt for every Codex session.

The [Anthropic evaluator agent file](../originals/vendor/anthropic-cwc/evaluator.md) combines instructions with metadata about a reviewer role and tools. Its accompanying [repository instructions](../originals/vendor/anthropic-cwc/CLAUDE.md) establish handoff conventions. Their [evidence-gate case](../cases/evidence-gate.md) explains how a runtime hook adds a check that prose alone cannot enforce.

## How to borrow a pattern honestly

First identify the job: generate, review, summarize, route, or execute. Then list the dependencies: input fields, files, tools, output parser, and stopping rule. Preserve the original separately if you adapt it. Describe the adaptation as yours, and test it in the environment where you intend to use it.

Changing the model, removing tools, or replacing the output parser creates a different system even if the prompt text stays identical. Public artifacts give us concrete engineering patterns to study; they do not justify claims about undisclosed private lab behavior.
