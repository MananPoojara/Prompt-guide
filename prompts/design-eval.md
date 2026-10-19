# Design a prompt evaluation

**Use:** Before comparing prompt variants.

## Copy and adapt

```text
Design an evaluation for [task]. Define the desired behavior and failure cases before seeing model outputs. Supply representative cases, a grading rubric, and a holdout strategy. Compare baseline and candidate with the same model, inputs, tools, and settings. Retain all runs, including errors and ties. Explain what the experiment cannot establish.
```

## Check the result

A failing example is rejected and a valid alternative is accepted.

## Watch for

A grader that rewards verbosity or exact wording unnecessarily.

Start with the shortest version that communicates the task. Add examples when ambiguity affects the result.

[Back to the library](README.md) · [Evaluation method](../guides/07-evaluations.md)
