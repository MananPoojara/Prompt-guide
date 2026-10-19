# Editorial review: YYYY-MM-DD

Copy this template into a new dated directory. Replace every placeholder with actual evidence; do not reuse a prior checked date as evidence of a new inspection.

## Reviewer and scope

State who performed the review, whether it was human or AI-assisted, the collection time, exact sources covered, and sources deliberately not checked. Do not call self-review independent review.

## Collect

Run `python3 scripts/source_watch.py --output /tmp/prompt-guide-review-YYYY-MM-DD` with an authenticated GitHub CLI, or download the hosted source-watch artifact. Preserve the original report in this review directory. Record failures as errors and retain prior baselines until the relevant change has been reviewed.

For each changed repository, inspect the comparison from its stored baseline to the reported commit. For websites and papers, retain the exact URL, version or publication date, access date, and the local claim it may affect. A repository HEAD comparison does not cover those sources.

## Triage

| Source/version | Local page or claim | Priority | Evidence examined | Decision | Remaining work |
|---|---|---|---|---|---|
| Fill with actual evidence | Link locally | Breaking / material / optional | Paths, diff, docs, execution | Integrate / no local change / investigate | Explicitly unverified items |

Check repository ownership and redirects. Distinguish official source material, partner contributions, and community examples rather than treating a publisher-owned repository as proof of every contained claim.

## Verify and integrate

Explain the change in the affected chapter or example, not only the update feed. State whether evidence was source inspection, offline replay, or a fresh execution. Preserve historical outputs. New model experiments need a protocol, fixed call/usage scope, and a new output directory.

Advance a source baseline only with a recorded review scope. An initial README-only baseline is a watch starting point, not whole-repository validation. Keep unreviewed content in the triage table even if its commit becomes the comparison baseline.

## Publish and carry forward

Run relevant tests plus `python3 evaluation/check.py --output /tmp/prompt-guide-review-checks.json`. Add a dated update linking local changes and this review. Confirm repository CI; link the exact run. If no local guidance changes, say so and state what was actually checked.

List unresolved research and the trigger for further work. Do not imply a daily collector performs this editorial process automatically. Keep a recurring human/maintainer reminder for the next review; this template creates no scheduled task by itself.
