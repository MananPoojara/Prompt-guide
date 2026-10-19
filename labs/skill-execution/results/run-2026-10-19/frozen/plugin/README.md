# A complete, small skill plugin

[Handbook explanation](../../handbook/05-skills-and-plugins.md) · [Start](../../START-HERE.md)

This is an authored Claude Code plugin containing one skill: inspect a claim against saved local evidence. It includes the [plugin manifest](.claude-plugin/plugin.json) and the complete [skill instructions](skills/inspect-evidence/SKILL.md).

From the repository root, with Claude Code installed:

```bash
claude --plugin-dir ./examples/claude-plugin
```

Then request:

```text
/prompt-guide:inspect-evidence Check the claim "the longer prompt is more accurate" against labs/prompt-contract/.
```

The plugin is loaded for that session through the local directory flag. The example does not install itself into global configuration. It does not include tools, hooks, MCP servers, credentials, or an external service. Its skill relies on the host's existing ability to inspect repository files.

## Validation status

On 2026-10-19, the skill passed the installed skill-creator frontmatter/name/description validator. The manifest was parsed as JSON, the installed Claude CLI plugin validator passed, and CLI help listed `--plugin-dir`. The validator also advised adding a marketplace install command; this sample deliberately uses a local directory and has no marketplace entry. **A model-driven invocation of the skill was not recorded.** The illustrated review in the handbook is authored explanation, not generated execution evidence.

A reader running this skill will use their own Claude Code runtime, model access, and usage. Inspect the short instructions before loading it. The [official plugin documentation](https://code.claude.com/docs/en/plugins) describes the package layout and namespaced skill invocation.
