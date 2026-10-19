# Start with something you can see

[View the full learning roadmap](ROADMAP.md) — foundations available now, advanced gaps stated explicitly.

You can read this repository without a model account, a coding background, or opening the external articles. The explanations below are written here; source links let you check where a claim came from. The original public prompts, selected source files, and recorded outputs are also stored here where redistribution is permitted.

Start with this sentence from a fictional meeting:

> Alex proposed November 5. No one accepted ownership or a deadline.

Ask an AI to turn it into a task list. Should Alex become the owner? Should November 5 become the deadline? If you have ever watched a fluent answer quietly turn a suggestion into a fact, you already understand the problem this resource addresses.

A useful prompt must communicate what counts as a correct answer. A useful AI system must also supply the right evidence, control what actions are possible, check results, and recover when something goes wrong. We will follow that progression with concrete files.

![From a question to an answer you can check](diagrams/request-map.svg)

## Start with a task you recognize

[Rewrite an email](everyday/writing/README.md), [summarize meeting notes](everyday/summarizing/README.md), [understand a fraction mistake](everyday/learning/README.md), [make a feasible plan](everyday/planning-clarification/planning.md), or [clarify a vague request](everyday/planning-clarification/clarification.md). Each has complete input, an exact prompt, an actual response, and a result check. No coding is required to read them.

For a visual explanation of model behavior, open the [tokenization and sampling lab](labs/model-mechanics/README.md). Its interactive page uses saved data and works offline. Developers can follow the [advanced lab path](labs/README.md) through representations, retrieval, output repair, and agent failures.

## Follow one connected explanation

| Read in order | What you will understand by the end |
|---|---|
| [1. Your first complete example](handbook/01-first-example.md) | Task, evidence, ambiguity, output format, and a real comparison that tied |
| [2. What the model receives](handbook/02-model-and-context.md) | Tokens, training, inference, context, roles, and why fluent text can be wrong |
| [3. Read an original lab prompt](handbook/03-original-prompts.md) | How to inspect published instructions without inventing an engineer's private workflow |
| [4. Give the model useful context](handbook/04-context-and-memory.md) | File selection, retrieval, memory, compaction, and a concrete handoff |
| [5. Skills and plugins, as files](handbook/05-skills-and-plugins.md) | A complete local skill, its plugin package, and what loading it does |
| [6. Tools and a real MCP connection](handbook/06-tools-and-mcp.md) | Tool schemas, arguments, execution, results, and a runnable local server |
| [7. Harnesses, loops, and graphs](handbook/07-harnesses-and-loops.md) | Who runs the loop, where state lives, and how retries stop |
| [8. Follow a coding change](handbook/08-coding-and-verification.md) | A request becoming code, tests, and a justified completion claim |
| [9. Evaluate and diagnose](handbook/09-evaluation-and-failures.md) | What a result proves, how comparisons fail, and which layer to repair |
| [Plain-language glossary](handbook/glossary.md) | Definitions with examples when a word is unfamiliar |

You do not have to finish this sequence before using the material. Each chapter includes the necessary example and points to its local evidence. A code block marked **illustration** is an explanation we wrote. A **recorded output** comes from a saved run. A **published original** comes from an identified upstream artifact.

## Enter through your immediate question

- “What should I type?” Read [the first example](handbook/01-first-example.md), then choose an [authored template](prompts/README.md).
- “What did lab engineers actually publish?” Open [the originals](originals/README.md) and [the annotated reading](handbook/03-original-prompts.md).
- “How can an AI use my tools?” Read [tools and MCP](handbook/06-tools-and-mcp.md), then run [the local connection](examples/mcp-notes/README.md).
- “Why did it say the work was done when it was broken?” Follow [the coding evidence](handbook/08-coding-and-verification.md) and [failure diagnosis](handbook/09-evaluation-and-failures.md).
- “How do longer agents work?” Follow [the loop diagram](handbook/07-harnesses-and-loops.md) and [the recorded evaluator case](cases/evaluator-loop/README.md).

## Ready to use an existing integration?

The [curated toolkit](toolkit/README.md) introduces five useful skill, plugin, and MCP options by task, with setup guidance and a first result to check. Start with one that solves a current need.

## How much should you trust this resource?

Trust the evidence at the level it supports. The saved note-extraction comparison contains eight task-level observations across two model responses. It cannot establish which prompt is best for everyone. The MCP example establishes that a client can discover and call a tool; it does not establish that a model will choose that tool wisely. The licensed original prompts establish what their publishers released at the recorded revisions; they do not reveal private conversations or every production configuration.

The repository keeps those limits next to the examples. Understanding the limit is part of understanding the technique.
