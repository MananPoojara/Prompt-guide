# Original public prompts

Read the actual artifacts, then inspect the system that used them. These are sourced from publisher-owned repositories, with pinned commits, byte hashes, and license copies. They are not recreated from screenshots, anonymous leaks, or our guess at an engineer's style.

| Original | What it actually is | Local evidence |
|---|---|---|
| [Anthropic generator](vendor/anthropic-cookbook/generator_prompt.txt) | Exact string from a runnable evaluator–optimizer notebook | Source inspected; generator execution not tested here |
| [Anthropic evaluator](vendor/anthropic-cookbook/evaluator_prompt.txt) | Exact evaluator string from that notebook | [Repeated local trials](../cases/evaluator-loop/README.md), using Codex rather than the original Claude runtime |
| [Anthropic independent reviewer](vendor/anthropic-cwc/evaluator.md) | Code with Claude 2026 event-demo agent instructions | Source inspected; full agent/hook integration not executed here |
| [Anthropic handoff conventions](vendor/anthropic-cwc/CLAUDE.md) | Repository instructions from the same event demo | Source inspected; depends on a configured harness |
| [OpenAI compaction](vendor/openai-codex/compaction.md) | Published Codex handoff-summary prompt | Source inspected; runtime behavior not reproduced here |
| [OpenAI Codex base prompt](vendor/openai-codex/gpt-5.2-codex_prompt.md) | Published model-specific agent instructions | Source inspected; not claimed to be the current default |

Also see the [exact task prompt used by an Anthropic Labs engineer](../cases/anthropic-game-maker.md), and the [autonomous-coding source note](autonomous-coding-source-note.md).

## What provenance proves

An official repository establishes who published the artifact and what the file says at a particular revision. It does not establish how often a specific employee uses it privately. An engineer's first-person experiment report establishes reported use in that experiment. A local reproduction establishes only what happened in our recorded environment.

[manifest.json](manifest.json) records source URLs, revisions, extraction details, licenses, and SHA-256 hashes. [Entries](entries.md) explain prerequisites and portability. The existing [template library](../prompts/README.md) is our authored material and is labeled accordingly.

## Reuse

Each vendor directory contains its upstream license; the OpenAI directory also retains NOTICE. Unmodified files remain unmodified. Notebook prompt strings are extracted as exact Python string values, including surrounding newlines; the original notebook is retained alongside them. Do not erase attribution or mix edits into these snapshots. Put adaptations in a separate file with a change description.

Run `python3 scripts/check_originals.py` to verify snapshots and extraction integrity locally. This checks bytes against the saved manifest; it does not independently re-fetch upstream or prove prompt quality.
