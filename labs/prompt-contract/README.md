# Lab: explicit extraction rules in Codex

**Question:** does stating how to handle unconfirmed information change the output on four simple task notes?

This is a small, executed tutorial comparison, with one attempt per variant. It is not a coding benchmark or a statistical estimate of prompt reliability. The candidate supplies missing policy details, so this compares specification completeness rather than isolating wording alone.

## Inspect the experiment

- [Baseline prompt](baseline.txt): asks for structured extraction.
- [Candidate prompt](candidate.txt): explicitly defines nulls, proposals, and superseded dates.
- [Expected output](expected.json): the rubric fixed before execution.
- [Actual baseline output](results/baseline.txt).
- [Actual candidate output](results/candidate.txt).

Both receive the same four cases: explicit commitment, missing information, an unaccepted proposal, and a changed deadline. Both use fresh Codex sessions in the same empty temporary working directory. No schema-enforcement flag is supplied. The model must satisfy the requested JSON format itself.

## Re-score locally

From the repository root, using Python 3:

```bash
python3 labs/prompt-contract/grade.py
python3 -m unittest discover -s labs/prompt-contract -p 'test_*.py'
```

The grader parses the entire response as JSON and checks exact object values and ordering. Extra or missing records fail the complete-output check. This narrow schema is appropriate for this extraction task; exact matching would be inappropriate for most prose tasks.

## Run new attempts

With a working Codex CLI login, from the repository root:

```bash
mkdir -p /tmp/prompt-guide-trial
codex exec --ignore-user-config --ephemeral --skip-git-repo-check --sandbox read-only -C /tmp/prompt-guide-trial --output-last-message /tmp/baseline-output.txt - < labs/prompt-contract/baseline.txt
codex exec --ignore-user-config --ephemeral --skip-git-repo-check --sandbox read-only -C /tmp/prompt-guide-trial --output-last-message /tmp/candidate-output.txt - < labs/prompt-contract/candidate.txt
```

Commands were checked against Codex CLI 0.163.0. Model calls consume account usage. Save new outputs separately and record the actual model and settings. `--ignore-user-config` does not promise a completely instruction-free runtime; Codex still supplies its own harness. These runs measure the model inside Codex, not a raw model API.

For a stronger experiment, pin the same available model for both variants, alternate order across repeats, use independent holdout notes, and report all runs. Do not overwrite these historical outputs to improve the result.

See [RESULTS.md](RESULTS.md) for the observed outcome and limitations.
