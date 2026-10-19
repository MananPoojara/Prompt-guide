# 5. Skills and plugins, as actual files

Previous: [Context and memory](04-context-and-memory.md) · Next: [Tools and MCP](06-tools-and-mcp.md)

A reusable workflow often needs more than a sentence. It might say which evidence to read, which questions to answer, and what form the result should take. A skill packages those instructions so an agent application can load them when relevant. A plugin packages capabilities for installation or distribution. Exact conventions depend on the host.

This repository includes a complete [Claude Code plugin example](../examples/claude-plugin/README.md). It is our authored educational example, not a copied lab prompt. Its job is narrow: inspect whether a claim is supported by local evidence.

## The package you can inspect

```text
examples/claude-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── inspect-evidence/
        └── SKILL.md
```

The [manifest](../examples/claude-plugin/.claude-plugin/plugin.json) names the package `prompt-guide` and gives it a version and description. The [skill file](../examples/claude-plugin/skills/inspect-evidence/SKILL.md) begins with a small metadata block, called frontmatter:

```yaml
---
name: inspect-evidence
description: Check a claim against saved local prompts, outputs, or test results. Use when the user asks whether repository evidence supports a statement about model performance or a coding result.
---
```

The description gives the host a reason to select the skill. The body gives the procedure once selected. This division avoids loading every possible workflow in full for every request. Loading and selection behavior are host-specific; a folder sitting in a repository is not proof that a particular application has activated it.

## What the skill actually asks the agent to do

The body asks the reviewer to separate four questions: what was supplied, what was observed, what independent check was performed, and how far the claim extends beyond the observations. It specifies five output fields: claim, evidence, verdict, safer wording, and missing check.

Those fields prevent a common shortcut: approving a broad statement because there is one impressive-looking response nearby. They also make the review useful to an author, because the reviewer must offer wording that preserves the supported finding.

For example, consider this claim:

> Our longer prompt is more accurate.

An **illustrative review**, not a recorded skill execution, would say:

```text
Claim: Our longer prompt is more accurate.
Evidence: Both saved outputs in labs/prompt-contract/results matched all four tasks.
Verdict: Unsupported by this comparison.
Safer wording: Both prompts succeeded on the four notes in one recorded trial each.
Missing check: A larger, independently written set and repeated controlled trials.
```

The skill cannot make the model infallible. It supplies a repeatable review procedure. A program checking the saved outputs still provides a different kind of evidence.

## Where a plugin fits

A plugin can bundle skills and other supported components such as hooks, agents, or MCP configuration. This sample contains only one skill. There is no hidden server, paid model trial, or background indexing task in it.

For a session-local Claude Code load, the official interface supports `--plugin-dir`. From this repository:

```bash
claude --plugin-dir ./examples/claude-plugin
```

Inside that session, the skill is namespaced by its plugin:

```text
/prompt-guide:inspect-evidence Check the claim "the longer prompt is more accurate" against labs/prompt-contract/.
```

This is an optional runtime example, requiring Claude Code and the account/runtime it uses. The repository records static validation separately from any actual skill invocation. The [native execution lab](../labs/skill-execution/README.md) now retains actual discovery and invocation events alongside a baseline review. See the [sample README](../examples/claude-plugin/README.md) for the validation status. The package layout and loading command follow the [official plugin documentation](https://code.claude.com/docs/en/plugins).

## Skill, instruction file, tool, and plugin are different objects

A repository instruction file describes conventions that apply within the host's configured scope. A skill describes a task-specific workflow. A tool is an operation the runtime can execute, with inputs and results. A plugin is a distribution package that may contain several of these components.

A skill can tell an agent to read test results, but it does not itself create a file-reading capability. A plugin can distribute an MCP server configuration, but credentials and execution permissions still need appropriate host handling. A tool's availability does not mean the model should call it for every request.

Use a skill when the procedure is useful across repeated tasks. Keep a one-off task in the current request when packaging would add no value. Put executable behavior in code and test it as code. Keep the instructions focused on the choices the agent must make around that behavior.
