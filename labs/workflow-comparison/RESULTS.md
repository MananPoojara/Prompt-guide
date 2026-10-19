# Recorded strategy comparison

Executed 2026-10-19. Two authored tasks, two repetitions per strategy. All twelve task runs and all 24 model calls are retained.

| Strategy | Answer checks | Resolved questions | Model calls | Median summed call seconds per task | Mean request characters per task |
|---|---:|---:|---:|---:|---:|
| single | 12/12 | 8/12 | 4 | 6.300 | 2298 |
| fixed | 12/12 | 8/12 | 4 | 6.939 | 1808 |
| agent | 12/12 | 8/12 | 16 | 26.205 | 10618 |

## Every run

| Run | Correct | Resolved | Calls | Summed call seconds | Request characters |
|---|---:|---:|---:|---:|---:|
| 1-routine-single | 3/3 | 3/3 | 1 | 17.268 | 2072 |
| 1-routine-fixed | 3/3 | 3/3 | 1 | 19.998 | 1583 |
| 1-routine-agent | 3/3 | 3/3 | 4 | 29.052 | 10263 |
| 1-conflict-single | 3/3 | 1/3 | 1 | 5.714 | 2523 |
| 1-conflict-fixed | 3/3 | 1/3 | 1 | 6.599 | 2034 |
| 1-conflict-agent | 3/3 | 1/3 | 4 | 26.489 | 10974 |
| 2-routine-agent | 3/3 | 3/3 | 4 | 25.921 | 10263 |
| 2-routine-fixed | 3/3 | 3/3 | 1 | 7.279 | 1583 |
| 2-routine-single | 3/3 | 3/3 | 1 | 6.101 | 2072 |
| 2-conflict-agent | 3/3 | 1/3 | 4 | 24.898 | 10974 |
| 2-conflict-fixed | 3/3 | 1/3 | 1 | 6.337 | 2034 |
| 2-conflict-single | 3/3 | 1/3 | 1 | 6.499 | 2523 |

All strategies tied on the authored reference checks. Each agent run used four calls; the other strategies used one. In the routine cases the agent searched, read the current plan, then performed another search before answering. The extra search did not improve the checked outcome. In the conflict cases it read both current documents and reported the contradiction. These observations do not establish the relative value of agents on tasks requiring adaptive actions.

Call durations include CLI/service overhead and are descriptive, not a stable speed estimate. Characters are not tokens or billing. The small tasks fit in a single request, metadata makes the fixed selection rule easy, and the labels have no independent human review. [Manifest and raw artifacts](results/pilot-2026-10-19/manifest.json).
