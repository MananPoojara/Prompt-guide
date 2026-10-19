# Design a tool contract

**Use:** When exposing a capability to an agent.

## Copy and adapt

```text
Specify a tool for [operation]. Define purpose, input types and validation, output structure, side effects, permission scope, and error categories. Include success, not-found, invalid-input, and transient-failure examples where relevant. Define retry behavior and an observable completion check. Keep the response limited to useful fields.
```

## Check the result

A caller can distinguish failure from a valid empty result.

## Watch for

Ambiguous errors causing unsafe retries.

Start with the shortest version that communicates the task. Add examples when ambiguity affects the result.

[Back to the library](README.md) · [Evaluation method](../guides/07-evaluations.md)
