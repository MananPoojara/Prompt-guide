# Review from a first-time reader's perspective

Reviewed 2026-10-19 by the repository authoring assistant. This is an editorial walkthrough using a beginner persona, not a usability study with independent participants.

The reader is assumed to have used a chat box but not to know JSON, context windows, skills, MCP, or agent runtimes. The review asks whether they can follow an example without opening external articles.

| Reader question / previous gap | Material now kept in this repository | Remaining limit |
|---|---|---|
| Where do I begin? | [Start page](../START-HERE.md) with ordered and question-based entry points | No independent reader timing study |
| What exactly should I type? | [Complete note task and prompt variants](../handbook/01-first-example.md) | One small recorded comparison |
| What does JSON/null mean? | Definitions next to a complete expected answer | Not a general programming manual |
| Does the model see all my files? | [Input/context explanation](../handbook/02-model-and-context.md) | Proprietary rendered requests may be hidden |
| Which prompts are actually from the publishers? | [Annotated reading](../handbook/03-original-prompts.md) plus licensed local originals | Private workflows are unavailable |
| How does stored memory become useful? | [Save/load/retrieval and handoff explanation](../handbook/04-context-and-memory.md) | Automatic recall has separate verification requirements |
| What files make a skill/plugin? | [Complete sample package](../examples/claude-plugin/README.md) | No recorded model-driven invocation |
| Can I see a real MCP exchange without paying for a model? | [Server, client, recorded result, setup](../examples/mcp-notes/README.md) | Local stdio only, no remote auth demonstration |
| Who controls the loop? | [State, routing, budgets, error paths](../handbook/07-harnesses-and-loops.md) | Pseudocode is labeled, not sold as a full agent SDK |
| How do I know the code works? | [Line-by-line saved coding example](../handbook/08-coding-and-verification.md) | Five checks, not exhaustive correctness |
| What should I fix when the answer is wrong? | [Failure diagnosis table](../handbook/09-evaluation-and-failures.md) | Hypotheses still require inspection |
| What does this unfamiliar word mean? | [Glossary](../handbook/glossary.md) | Provider-specific meanings can differ |

The expansion adds original explanations, a local diagram, and runnable example code. It does not mirror complete third-party articles. External references establish provenance and let readers investigate further; they are not required reading for the connected handbook.
