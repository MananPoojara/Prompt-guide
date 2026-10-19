# 1. Turn an intention into a contract

A useful prompt tells the assistant what a successful result looks like. “Act like a senior engineer” can set a tone, but it leaves the actual problem unspecified. Begin with the observable change you need.

## A worked example

**Before — underspecified prompt**

```text
Make the search better.
```

**After — original template, not a recorded model run**

```text
In this repository, make product search ignore leading/trailing whitespace
and match names without case sensitivity.

Inspect the current search implementation and existing tests first.
Preserve the existing sorting, pagination, and empty-query behavior.
Use the repository's conventions and avoid new dependencies for this change.

Verify: "  LAMP " matches the same products as "lamp"; an unknown product
returns the existing empty state; pagination and sorting still work.
Run the relevant tests and report the files changed, actual results, and
anything you could not verify. Implement the change.
```

The added information resolves four decisions: what “better” means, where to look, which behavior to preserve, and what evidence will count. It does not prescribe a particular function or library before inspecting the project.

**Expected review evidence, not fabricated output:** the implementation diff, a test covering normalization, a regression check for existing search semantics, and the commands actually run. A polished summary alone does not satisfy the contract.

## Build your own

```text
Outcome: [observable behavior or artifact]
Context: [relevant files, examples, sources, or reproduction steps]
Constraints: [compatibility, scope, dependencies, audience]
Verification: [specific checks and the evidence to return]
```

Remove fields that do not affect the answer. A one-line rewrite usually needs much less detail than a database migration. Ask questions when a missing answer changes the design; allow routine implementation decisions to follow repository conventions.

## Diagnose a disappointing response

| Symptom | First experiment |
|---|---|
| Correct-looking answer about the wrong problem | Add an input/output example |
| Unwanted rewrite | Identify the behavior and interfaces to preserve |
| Confident invented fact | Supply sources and specify what to do when evidence is missing |
| Endless planning | State whether you want a proposal or implementation |
| “Done” without evidence | Name the check and require the actual result |


Public grounding: [OpenAI prompting guidance](https://developers.openai.com/api/docs/guides/prompting) encourages task-specific details and examples plus prompt evaluation. The four-field contract here is our teaching framework, not an official lab standard.

Next: [Model behavior](02-model-behavior.md).
