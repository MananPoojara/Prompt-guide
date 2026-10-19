# Coding lab: normalize product search

This is an **executed Codex coding demonstration**, not a comparison between two prompts. It shows how a concrete task and observable checks lead to a reviewable change.

## What happened

The original function used case-sensitive substring matching. The prompt asked Codex to trim query whitespace, match without case sensitivity, preserve order and empty-query behavior, and keep tests unchanged.

- [Exact prompt](prompt.txt)
- [Original implementation](before.py)
- [Resulting implementation](after.py)
- [Unchanged tests](test_search.py)
- [Actual model response](response.txt)
- [Before test output](before-tests.txt): 2 passed, 3 failed.
- [After test output](after-tests.txt): 5 passed, 0 failed.

The model used `strip()` on the query and `casefold()` on both query and names. An independent post-run test execution confirmed all five tests pass, and a byte comparison confirmed the test file was unchanged.

Executed 2026-10-19 using Codex CLI 0.163.0, `gpt-6.1-sol`, reasoning effort `none`, with user config ignored and a workspace-write sandbox in a disposable directory. One model attempt; no retry selection. The raw response refers to the temporary execution path, which is not a portable repository link.

## Reproduce the code checks without a model

From the repository root:

```bash
trial_dir=$(mktemp -d)
cp labs/search-fix/test_search.py "$trial_dir/test_search.py"
cp labs/search-fix/before.py "$trial_dir/search.py"
(cd "$trial_dir" && python3 -m unittest -v)
# Three failing tests above are expected for the original implementation.
cp labs/search-fix/after.py "$trial_dir/search.py"
(cd "$trial_dir" && python3 -m unittest -v)
```

To make a new model attempt, copy `before.py` as `search.py` alongside the tests in a new disposable directory. Start Codex there and paste `prompt.txt`. Preserve the new output separately.

## What this establishes—and what it leaves open

The resulting code meets the five demonstrated checks. This does not prove arbitrary Unicode search semantics, performance at scale, or correctness inside a full product with pagination and persistence. No model or prompt superiority is established. The example is intentionally small enough for a learner to inspect every line.
