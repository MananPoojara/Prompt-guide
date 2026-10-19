# Contributing

Contribute a specific lesson, prompt, counterexample, or measured result. Include enough context for someone else to check it.

## Evidence requirements

- Link primary sources for factual claims and record when they were checked.
- Distinguish a documented claim, your inference, an illustration, and an executed result.
- For experiments, retain prompts, inputs, raw outputs, model and harness metadata, grading rules, and all failures. Never fabricate a before/after transcript.
- Explain the task distribution and limitations before generalizing a score.
- Remove credentials, customer data, and private workspace details before publishing traces.

## Review process

Check relative links, read the rendered Markdown, run the relevant lab grader, and inspect the changes against the original objective. Explain what the contribution changes for a learner. Keep unrelated changes separate.

## Maintenance

Follow the [weekly editorial review procedure](updates/README.md), and prioritize known breaking changes when discovered. Update the affected explanation alongside the dated update entry. Recheck conceptual claims when conflicting research appears. Preserve historical experiment metadata and record corrections explicitly. A daily nine-repository source collector is configured and has been verified in GitHub Actions. One editorial pass is recorded; ongoing weekly continuity remains unproven. The collector does not publish guidance automatically.

## Original prompts and case studies

Prefer publisher-owned repositories or a named engineer's first-person account. Record the exact revision, runtime role, required context/tools, and evidence of use. Preserve licenses and notices. Do not attribute our paraphrases to an engineer. For unclear licensing, document the ambiguity and link the source instead of silently republishing it.

A strong case includes the original prompt, assembled input, tool/runtime conditions, observed output, verification artifact, and a diagram of the relevant flow. A source-inspected artifact may be useful without a local reproduction; label that status plainly. Keep source bytes unchanged and adaptations separate.

Archived model inputs and logs retain their original whitespace. The results directory's Git whitespace attribute prevents formatting checks from encouraging edits to historical evidence; source and authored documentation still use normal checks.

## Reader and label feedback

Use the [reader review packet](review/README.md) or the separate [annotation packet](labs/natural-notes/review/README.md). These are unfinished human-review gates, not completed studies. Disclose assistance and prior exposure to reference answers; obtain consent before publishing private feedback.

## License

Submit original contributions under the project's [MIT License](LICENSE). For third-party material, identify its source and retain its applicable license and notices; do not relicense it as your own contribution.
