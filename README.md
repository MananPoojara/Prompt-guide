<p align="center">
  <img src="assets/prompt-guide-header.svg" alt="Prompt Guide — Understand the prompt. See the system. Check the result." width="960">
</p>

<p align="center">
  <strong>A practical, open resource for learning how prompting and AI agents work.</strong><br>
  Original public prompts. Clear explanations. Real outputs you can inspect.
</p>

<p align="center">
  <a href="https://github.com/MananPoojara/Prompt-guide/actions/workflows/checks.yml"><img src="https://github.com/MananPoojara/Prompt-guide/actions/workflows/checks.yml/badge.svg" alt="Repository checks"></a>
  <a href="START-HERE.md"><img src="https://img.shields.io/badge/start_here-beginner_friendly-6ee7b7?style=flat&amp;labelColor=18212b" alt="Start here — beginner friendly"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/contributions-welcome-9bb9f3?style=flat&amp;labelColor=18212b" alt="Contributions welcome"></a>
</p>

<p align="center">
  <a href="START-HERE.md"><strong>Start reading</strong></a> ·
  <a href="originals/README.md">Original prompts</a> ·
  <a href="cases/README.md">Recorded examples</a> ·
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

## Start here

**[Open the beginner guide →](START-HERE.md)** No installation or model account needed. The explanations, examples, diagrams, and glossary are in this repository.

Want a local copy?

```bash
git clone https://github.com/MananPoojara/Prompt-guide.git
cd Prompt-guide
```

Then open `START-HERE.md` in your editor or Markdown viewer.

## What it does

Prompt Guide helps you understand what to ask a model, what information it needs, how it uses tools, and how to check its work. Follow a simple meeting-note example through prompts, context, memory, skills, MCP, and agent loops.

You can also inspect **six original public prompt artifacts from Anthropic and OpenAI**, with their source revisions and licenses, alongside recorded local experiments. Our explanations and templates are labeled separately.

## See the difference

A useful prompt makes the decisions behind a task explicit. Here is an **authored illustration** using the notes in our extraction example:

| A broad request | A request with clear decision rules |
|---|---|
| “Turn these meeting notes into tasks.” | “Extract confirmed owners and deadlines. Keep proposed or unassigned values as `null`. A changed deadline replaces the earlier date. Return one record per task.” |
| Leaves “owner,” “deadline,” and missing values open to interpretation. | Defines how to handle proposals, missing information, and changed dates. |

Given **“Alex proposed November 5. No one accepted ownership or a deadline,”** the intended record keeps both owner and deadline unconfirmed.

**Did more detail improve the measured result?** In our separate [recorded comparison](labs/prompt-contract/RESULTS.md), both the shorter and longer prompts got all four records right. The prompts, raw responses, and checker are saved. A clearer rule is useful to understand; an accuracy improvement still needs evidence.

## What's inside

| Explore | What you get |
|---|---|
| [Beginner handbook](START-HERE.md) | Nine connected chapters, diagrams, and a plain-language glossary |
| [Original public prompts](originals/README.md) | Six licensed artifacts with exact revisions, hashes, and context |
| [Recorded cases](cases/README.md) | Actual inputs, feedback, generated revisions, and independent checks |
| [Reusable prompt templates](prompts/README.md) | Twelve authored starting points with checks and failure modes |
| [Working examples](examples/README.md) | A local MCP server/client and a complete skill/plugin package |

<details>
<summary><strong>Browse the handbook chapters</strong></summary>

1. [Your first complete example](handbook/01-first-example.md)
2. [What the model receives](handbook/02-model-and-context.md)
3. [Read an original lab prompt](handbook/03-original-prompts.md)
4. [Give the model useful context](handbook/04-context-and-memory.md)
5. [Skills and plugins, as files](handbook/05-skills-and-plugins.md)
6. [Tools and a real MCP connection](handbook/06-tools-and-mcp.md)
7. [Harnesses, loops, and graphs](handbook/07-harnesses-and-loops.md)
8. [Follow a coding change](handbook/08-coding-and-verification.md)
9. [Evaluate and diagnose](handbook/09-evaluation-and-failures.md)

Keep the [glossary](handbook/glossary.md) nearby when a term is unfamiliar.

</details>

## Follow a real run

Anthropic's published evaluator prompt reviewed a small stack implementation with a duplicate-minimum bug. Its feedback was passed to the published generator prompt through our local Codex runtime. The generated revision then received independent behavior checks and a fresh evaluation.

[Read the complete case, including inputs and raw outputs →](cases/evaluator-loop/README.md)

![Original prompt, recorded feedback, generated revision, and independent checks](diagrams/evaluator-case.svg)

The defective fixture received FAIL in three trials; the comparison fixture received PASS in three. The feedback also exposed an ambiguity about time complexity. This is a small local reproduction using Codex, with its limits documented in the case.

## Try it yourself

Recheck saved evidence with Python 3. These commands use the standard library and do not call a model:

```bash
python3 scripts/check_links.py
python3 scripts/check_originals.py
python3 labs/prompt-contract/grade.py
python3 -m unittest discover -s cases/evaluator-loop -p 'test_*.py'
```

For a live tool connection, run the **[local MCP example](examples/mcp-notes/README.md)**. It includes dependency setup, a server, a client, and recorded output. No model API key is needed.

The **[skill/plugin example](examples/claude-plugin/README.md)** shows the complete package and optional Claude Code loading command. It passed static validation; a model-driven invocation has not been recorded. Fresh model trials use your own runtime and usage budget.

## How we label evidence

- **Published original:** released by the named publisher, preserved with attribution.
- **Reported experiment:** described by the original author; not reproduced here.
- **Executed here:** inputs, outputs, runtime details, and checks are saved.
- **Our synthesis:** an explanation, diagram, adaptation, or template we authored.

Browse the [source ledger](research/sources.md), [claim checks](research/claims.md), and [reader review](research/reader-review.md). This project is independent of OpenAI and Anthropic. Public artifacts do not reveal undisclosed private lab workflows.

## Contributing

Found a confusing explanation, a useful public prompt, or a counterexample? **[Read the contribution guide](CONTRIBUTING.md)** and [open an issue](https://github.com/MananPoojara/Prompt-guide/issues).

Include the source or relevant files, explain what a reader should learn, and keep observed results separate from expectations. Failed runs and ties are useful contributions too.

## Credits and reuse

Original artifacts retain their upstream licenses and notices. See the [originals directory](originals/README.md) for attribution and file-specific reuse terms. A repository-wide license for the authored material has not yet been selected; upstream licenses apply to their respective artifacts.

Sources last inspected: **2026-10-19**. [Project history](FLOW.md) · [Memory records](memory/README.md)
