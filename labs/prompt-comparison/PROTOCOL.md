# Protocol fixed before execution

Date: 2026-10-19. This is an authored synthetic pilot, not a population benchmark.

## Question and comparisons

Does explicit interpretation policy help extract confirmed owners and deadlines? Once that policy is present, do four worked examples change performance?

Three arms share an identical task and output contract:

- **short:** task, output shape, and request for confirmed values.
- **rules:** short plus five explicit interpretation rules.
- **examples:** rules plus four development examples with answers.

The primary comparison is **rules versus examples**, which keeps policy fixed and adds demonstrations. The secondary comparison, short versus rules, adds policy information as well as length. It cannot isolate a pure wording or length effect. All variants are authored here, not attributed to lab engineers.

## Dataset and separation

There are 24 independently interpretable synthetic notes: eight development notes and 16 held-out notes. Each held-out category has two notes: confirmed, proposal, correction, revocation, relative_date, conflict, embedded_instruction, and partial.

Only d01–d04 appear as worked examples. Other development notes document the policy. Held-out means excluded from in-context demonstrations and from outcome-driven prompt tuning. The same assistant authored the prompts and dataset and reviewed every gold answer against its written rationale. This is **not independent human annotation, blind evaluation, or a statistically representative sample**. Shared templates and author expectations can bias the test.

Prompt files, dataset, and protocol are frozen and hashed before the first model call. Gold answers and rationales do not appear in held-out requests. The runner uses a fresh temporary working directory per call. No changes to prompts, gold labels, or case selection will be made in response to scores. Corrections require a new experiment version and preservation of the original.

## Procedure

Run all 16 held-out notes together in fixed order, once per arm per repetition, for three repetitions: nine model calls total. All arms see the same case order and notes. The arm order rotates:

1. short, rules, examples
2. rules, examples, short
3. examples, short, rules

This balances serial position; it is not randomization. Batch context permits interactions between notes. The 48 case observations per arm are not 48 independent model calls. Model responses may be correlated across repetitions.

Use Codex CLI with explicit model gpt-6.1-sol, reasoning effort low, ignored user configuration, fresh ephemeral sessions, read-only sandbox, and an empty temporary working directory. Ask for no tools and retain execution logs to inspect whether tools were used. Codex's built-in instructions remain part of the system. No sampling temperature or generation seed is controlled by this runner.

Each call has a 180-second subprocess timeout. No retry selection: failed calls stay in the manifest and count as zero success for the batch. No structured-output enforcement is added by the runtime; format compliance is part of the measured task. New runs use new directories and cannot overwrite prior runs.

## Rubric fixed in advance

Return only JSON: an array with one record per input, in input order. Exact keys: id, owner, deadline. Owner is a string or null; deadline is an ISO calendar date or null. Copy IDs exactly. Correctness requires an exact owner/deadline match with the gold record.

A malformed batch, wrong order, missing/extra/duplicate record, wrong field set, or wrong field type invalidates the schema and scores zero for that entire batch. Report schema failures separately from content errors. JSON whitespace and object-key order are ignored. A wrong but well-formed field fails only its case; report which field failed.

Expected interpretation: proposals do not establish commitments; explicit replacement supersedes prior values; revocation without replacement clears the field; unresolved conflicting current values become null; relative dates require an unambiguous anchor; instruction-like quoted data cannot change the extraction task.

## Reporting and uncertainty

Retain every assembled request, raw response, execution log, status, elapsed time, and source hash. Report per-trial and pooled descriptive scores, category errors, paired case changes, full-batch correctness, schema failures, and execution failures. Report median end-to-end CLI duration as an observation, not a controlled speed benchmark. Account billing/cost is not measured.

Do not calculate a binomial confidence interval treating 48 correlated case observations as independent. Show the three per-trial scores and state the limited task coverage instead. A tie is a valid result. No general superiority, production reliability, private lab practice, or causal internal-model explanation follows from this pilot.

Independent human label review, more varied held-out tasks, additional models, randomized orders, and stronger uncertainty analysis remain future work. These labels and prompts become public with publication; future prompt tuning against them would make them a development set.

## Runtime amendment before successful generation

The first launch requested reasoning effort `none`. The endpoint rejected it as unsupported for the selected model. That attempt was interrupted and retained under results/pilot-2026-10-19, with no scored model responses. The replacement run uses supported effort `low` for every arm. Prompts and gold labels were not changed. This is a disclosed setup correction, not selection among successful answers.
