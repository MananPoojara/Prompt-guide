# Watch a skill load in its actual host

[Developer lab path](../README.md) · [Sample plugin](../../examples/claude-plugin/README.md) · [Skills chapter](../../handbook/05-skills-and-plugins.md)

A `SKILL.md` file is a procedure, not an executed result. This lab records the sample plugin being loaded and invoked through Claude Code's native skill mechanism, then compares its review with a baseline session that has skills disabled.

The task is to check the claim “the longer prompt is more accurate” against the repository's saved four-case prompt-contract experiment. Both sessions receive the same evidence files in fresh temporary directories. They can read files but cannot run new experiments or write through their available tools.

## What actually loaded and ran

Executed 2026-10-19 with Claude Code **2.1.303**, low effort. The requested model alias `sonnet` resolved to **`claude-sonnet-5-5` in both recorded sessions**. This identifies the observed runtime; it is not a recommendation or a claim that the alias will resolve identically later.

| Check | Baseline | Plugin condition |
|---|---|---|
| Custom plugin | Not loaded | `prompt-guide`, version 0.1.0 |
| Skill discovery | Skills disabled | `prompt-guide:inspect-evidence` listed |
| Native invocation | None | Successful `Skill` call and launch receipt |
| Evidence reads | Saved prompts, outputs, rubric, grader and summaries | Same core evidence plus grader tests |
| Substantive conclusion | Claim unsupported; observed tie | Claim unsupported; observed tie |
| Five named review sections | Not required | Claim, Evidence, Verdict, Safer wording, Missing check |
| Evidence-file hashes after review | Unchanged | Unchanged |

The [filtered native transcript](results/run-2026-10-19/skill.events.json) contains the discovery metadata, actual `Skill` invocation, successful launch receipt, and subsequent file reads. The [skill response](results/run-2026-10-19/skill.output.txt) and [baseline response](results/run-2026-10-19/baseline.output.txt) are retained verbatim as final text. Neither session ran the grader; both inspected its code and saved evidence. We separately verified that the saved outputs match each other and that the referenced grader tests exist.

## What the comparison does—and does not—show

The native loader worked, the skill was invoked, and the response followed its requested structure. Both sessions reached the same useful conclusion. There is no measured accuracy advantage here.

The baseline disables all skills, while the plugin condition exposes the skill interface and the host's available built-in skill catalog. Built-in plugins remain in both initialization records. Thus, this is a procedural demonstration with different invocation/context paths, not an isolated causal test of one instruction or a clean raw-model experiment.

The model reviews are observations, not independent human review. In particular, the skill response repeats the documented rubric chronology without independently proving when the rubric was created. A model's confident wording should not be promoted into stronger provenance than the files establish.

The CLI reported estimated session costs of **USD 0.0385399** for baseline and **USD 0.0574511** for the skill condition. These are provider-reported runtime estimates, not verified invoices or evidence of a stable cost difference. Both sessions had a USD 1 CLI cap and a 240-second process timeout. One session per condition is insufficient for performance conclusions.

## Reproduce the native invocation

The recorder requires an installed, authenticated Claude Code runtime with access to its selected model. It consumes account usage. Use a new output directory:

```bash
python3 labs/skill-execution/run.py --output /tmp/native-skill-run
```

The recorder copies the evidence and plugin into temporary working directories. It uses `--plugin-dir` for session-only loading, restricted read-only tools, `--strict-mcp-config`, disabled hooks for the run, and no persistent session. It does not install or change global plugin configuration. Managed host policies may still apply; the recorded initialization shows the actual available tools/components. [Official local-plugin documentation](https://code.claude.com/docs/en/plugins) · [Hook override behavior](https://code.claude.com/docs/en/hooks#disable-or-remove-hooks).

The original prompt, exact command, CLI version, source hashes, and initialization metadata are in the [manifest](results/run-2026-10-19/manifest.json) and event files. The [protocol](PROTOCOL.md) declared the two-session scope before execution.

## Transcript handling and verification

The published event files are **filtered transcripts**, not complete raw protocol streams. They retain initialization model/tool/skill/plugin data, text, tool calls/results, and final accounting. Reasoning/signature blocks and top-level account/session metadata are omitted by an explicit allowlist. Unfiltered streams were kept in private temporary directories and are not committed. Final-response text is unchanged.

Offline checks require Python 3.10+ only:

```bash
python3 -m unittest discover -s labs/skill-execution -p 'test_*.py'
python3 labs/skill-execution/check_saved.py
```

The checker verifies discovery and successful invocation rather than merely searching the final answer for a skill name. It also checks evidence reads, unchanged source hashes, final-result integrity, and the requested section labels. That last check validates format, not semantic correctness. The complete procedure remains short enough to inspect in the [original skill file](../../examples/claude-plugin/skills/inspect-evidence/SKILL.md).
