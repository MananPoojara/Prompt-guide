# Verification record — 2026-10-19

- Initial full recording: clean Python 3.10.12 environment with pinned dependencies, CPU, all five conditions retained.
- Separate system Python reproduction: query vectors and every chunk vector matched exactly; all rankings and evidence metrics matched. BM25 summation order changed only last-bit scores, within the documented tolerance.
- Ten standard-library tests passed. Coverage 7.16.2 measured 100% statement coverage for the 42-statement `retrieval.py` ranking/metric module. This is not whole-project coverage or a measure of retrieval quality.
- Offline artifact checker passed for all five conditions. CLI result viewer exercised the duplicate-write example with both small and large windows.

## Setup failure retained as a development finding

The first separate-environment reproduction failed before model loading with:

```text
AttributeError: module 'inspect' has no attribute 'signature'
```

The newly added local viewer was named `inspect.py`, shadowing Python's standard-library module during a Torch import. It was renamed to `view_results.py`, and a fresh output directory was used for the successful reproduction. This was an application packaging failure, not an encoder or retrieval-quality failure. The initial experimental recording had finished before the viewer was added and was unaffected.
