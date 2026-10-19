# Planning and clarification: complete recorded examples

[Everyday examples](../README.md) · [Planning](planning.md) · [Clarification](clarification.md)

These two fictional scenarios complete the everyday entry path. Each page includes the supplied material, exact request, actual response, explicit checks, and a labeled failure illustration. Reading needs no coding knowledge or model account.

Three responses were recorded on 2026-10-19 using Codex CLI with requested model `gpt-6.1-sol`, low reasoning effort, fresh ephemeral sessions, ignored user configuration, and a read-only sandbox. The [manifest](results/run-2026-10-19/manifest.json) retains the CLI version, exact commands, statuses, durations, and input/output hashes. Source files and the [predeclared protocol](PROTOCOL.md) are frozen with hashes.

The planning task has fixed estimates and dependencies. The clarification example includes an authored user reply frozen before execution; it is not a genuine user interview. All three processes succeeded. Responses are unedited, and checks on the pages are explicitly attributed to the authoring assistant. Independent human review remains pending.

## Verify integrity offline

Python 3.10+ only:

```bash
python3 everyday/planning-clarification/check_saved.py
```

This verifies source and response hashes and reconstructs the exact inputs, including the scripted conversation. It checks artifact integrity, **not semantic correctness**. The arithmetic and factual checks appear on the example pages so readers can inspect them directly.

## Record a new run

An authenticated Codex CLI with model access is required. This consumes account usage: at most three calls, each with a 180-second timeout, no retries, and no enforced dollar cap. Use a fresh destination:

```bash
python3 everyday/planning-clarification/run.py --output /tmp/planning-clarification-new-run
```

A fresh session is used for each call. The third request embeds the previous question and response as text. Hidden reasoning and private account metadata are omitted from the recording.

These are successful demonstrations, not a controlled comparison of prompt quality. One run does not establish reliability across models, future versions, or real-world schedules. For your own task, recheck the answer against your actual constraints.
