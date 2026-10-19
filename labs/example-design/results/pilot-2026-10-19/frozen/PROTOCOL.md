# Protocol fixed before generation

2026-10-19. Authored synthetic extraction pilot, not an independent benchmark.

Ten evaluation notes are new to this experiment. Four separate demonstration notes provide two simple and two boundary examples. One assistant authored notes, policy, labels, and rationales. Evaluation notes and their labels are frozen before execution; they are excluded from demonstrations, not independently held out by a reviewer. Policy and scoring are reused from the earlier extraction lab.

Five conditions:

1. `none`: shared rules, no demonstrations.
2. `simple`: shared rules plus d1,d2.
3. `boundary`: shared rules plus d3,d4.
4. `reversed`: shared rules plus d4,d3, changing only demonstration order relative to boundary.
5. `decomposed`: one call builds an explicit evidence ledger from the original notes; a fresh second call receives shared rules, d3,d4, and the ledger, without the original notes.

Selection comparison: simple versus boundary has equal example count but different information, difficulty, and text length. It is not equal-token or pure order manipulation. Order comparison: boundary versus reversed retains identical examples and task cases. Decomposition comparison: boundary versus decomposed compares complete pipelines, including an extra call, changed representation, and loss of access to the originals. It is not an isolated "think step by step" wording test or a claim about hidden reasoning.

Two repetitions of all five conditions. First order: none, simple, boundary, reversed, decomposed. Second order: simple, boundary, reversed, decomposed, none. This rotation does not fully counterbalance five serial positions. All ten notes appear in fixed order in each batch, so outcomes within a batch are correlated. No temperature or generation seed is controlled.

At most 12 model calls, each with a 180-second timeout, no retry. Fresh empty temporary working directories; Codex ephemeral, ignored user configuration, read-only sandbox, requested model gpt-6.1-sol, reasoning effort low. Account usage required; no enforced dollar cap or invoice data. Retain final responses, exact inputs, commands, process statuses, and durations; omit hidden reasoning and private account metadata.

The decomposition ledger is an inspectable intermediate work product, not a reasoning transcript. It is not automatically corrected. If the ledger call fails, skip the answer call and score zero. If it succeeds, pass its exact output to the answer stage, even if malformed. Report that limitation and inspect lost or invented facts manually; a production pipeline should validate intermediate representations. The two-stage run does not inherit a conversation session between calls.

Final scoring reuses the existing strict batch contract: exact ordered IDs and id/owner/deadline keys, owner string or null, real ISO calendar date or null. Duplicate JSON keys or invalid schema invalidate the batch. Otherwise score each owner/deadline pair against the frozen reference. Failed final calls score zero even if a partial output exists. Preserve original outputs and labels; corrections require a separately labeled amendment.

Report each repetition, exact-batch successes, schema/process failures, per-case errors, paired changes for the selection/order/decomposition comparisons, call counts, and summed durations. No independence-based accuracy confidence interval, population superiority claim, independent review, or causal internal-model explanation follows from this small study. Ties are valid results; do not manufacture a gain by retuning or dropping cases.
