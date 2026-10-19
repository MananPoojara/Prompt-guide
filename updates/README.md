# What's new, and what still holds up?

[Main guide](../README.md) · [Learning roadmap](../ROADMAP.md) · [Source ledger](../research/sources.md)

This page is the home for reviewed updates to Prompt Guide. Each entry should explain the change, who it affects, what action a reader should take, and the evidence behind it. Readers should be able to understand the practical change here; external links provide provenance and further detail.

**Cadence:** a weekly editorial review is planned. No recurring scan, scheduled publishing job, or automatic model experiment is currently configured. This page does not claim continuous monitoring or coverage of every release.

## Published updates

| Date | Update | What changed |
|---|---|---|
| 2026-10-19 | [Foundations and first controlled pilot](2026-10-19.md) | Current learning material, measured results, and the next development priorities |

## What belongs in an update?

- A documented model or API change that affects an existing example or recommendation.
- A skill, plugin, or MCP change that affects setup, compatibility, or behavior.
- A new research finding with a practical implication and clearly stated limits.
- A reproduced result, correction, regression, or newly discovered failure in this repository.
- A new self-contained explanation or demonstration that fills a roadmap gap.

A launch announcement alone is not evidence of improved performance. A release with no relevant change need not become a recommendation. If a review finds nothing that changes the guide, publish a short “reviewed, no material change” entry with the actual scope checked.

## Weekly review procedure

1. **Collect:** inspect primary documentation, release notes, publisher-owned repositories, and relevant papers. Start with the existing source ledger and toolkit records; expand coverage when the guide needs it.
2. **Triage:** identify which local pages, commands, examples, or claims could be affected. Separate breaking changes, practical improvements, and findings that need investigation.
3. **Verify:** inspect the underlying source. Rerun the affected example where feasible. Record source-only review separately from execution; do not silently imply one proves the other.
4. **Integrate:** update the actual chapter or example, not only this feed. Preserve old experimental artifacts. Link the replacement explanation, and document any changed recommendation.
5. **Publish:** add a dated update after applicable checks pass. Include uncertainties and any reader action. Keep unfinished research in the roadmap rather than presenting it as a completed result.

The maintainer owns each review; contributors can submit evidence and corrections. Independent human review must be credited as such only when it actually occurs. New paid model runs require a defined experiment and usage scope; a documentation check is not authorization for unlimited benchmarking.

## Required entry fields

| Field | Reader question it answers |
|---|---|
| Change and affected audience | What happened, and does it matter to me? |
| Practical explanation | What should I understand without opening another article? |
| Local pages affected | Where is the corrected or expanded guidance? |
| Evidence status | Source-inspected, locally executed, or provisional? |
| Source and version | Which document, release, model, or commit supports it? |
| Checked date | When was this actually reviewed? |
| Action and limits | What should I do, and what remains uncertain? |

## Freshness and corrections

A last-checked date records an actual inspection, not a guarantee of current correctness. Do not refresh dates merely because a week passed. Keep a recommended command's host and version assumptions beside it. Flag known breakage promptly and remove unusable recommendations from the starter shortlist until repaired.

When evidence changes a conclusion, explain the old statement, the corrected statement, and why it changed. Never overwrite raw model outputs to make a historical result match the new conclusion.

Future automation may collect changed sources and open a review queue. It should not turn a changed page into an automatic endorsement or publish unreviewed generated advice. Automation status will be stated here when implemented.

## Follow along

Use GitHub's Watch controls to choose repository notifications, or revisit this index. There is no separate newsletter or external subscription required. Suggestions should include a primary source and the local guidance they affect; see [contributing](../CONTRIBUTING.md).
