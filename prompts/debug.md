# Debug with evidence

**Use:** For a reproducible failure.

## Copy and adapt

```text
Investigate this failure: [symptom and reproduction]. Establish the observed and expected behavior. Trace the relevant code and test the most likely cause. Make a focused fix and verify the original reproduction plus relevant regressions. Distinguish an environment failure from a product defect. Report the cause with evidence; do not claim a test ran if it did not.
```

## Check the result

The original reproduction fails before the fix and passes afterward.

## Watch for

Guessing a cause from an error message alone.

Start with the shortest version that communicates the task. Add examples when ambiguity affects the result.

[Back to the library](README.md) · [Evaluation method](../guides/07-evaluations.md)
