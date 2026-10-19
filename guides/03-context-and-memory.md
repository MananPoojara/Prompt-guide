# 3. Give the agent the right context at the right time

Separate stable working agreements from task-specific facts. The current task should explain what to achieve; repository instructions should explain enduring conventions; research records should explain what is known and where it came from.

| Information | Suggested home | Revalidation |
|---|---|---|
| Build and test commands | Repository instructions | When tooling changes |
| Current task and acceptance criteria | Task prompt or issue | On scope changes |
| Design decision and reason | Decision note | When constraints change |
| Source-backed finding | Research ledger | On review date or conflicting evidence |
| Run status and next action | Handoff note | At resume, against real files |
| Credentials | Secret store | Never copy into prompt libraries |

Codex documents layered `AGENTS.md` discovery, including more specific instructions along the project path. Keep these files short and verify which apply to your working directory. [Official instructions documentation](https://developers.openai.com/codex/guides/agents-md)

## Original repository instruction example

```markdown
# Working agreements
- Follow the existing module boundaries and naming conventions.
- For behavior changes, run the relevant tests and report actual results.
- Preserve public interfaces unless the task explicitly changes them.
- Record unresolved assumptions in the final handoff.
```

Add real setup commands after inspecting the repository. Do not paste invented `npm test` commands into a Python project.

## A context packet for coding

```text
Goal: make export headers stable across repeated runs.
Read: the export implementation, its tests, and the current format specification.
Authority: the current specification supersedes archived examples.
Known failure: the same fixture produces different column ordering.
Evidence needed: two runs over the same fixture produce identical headers.
```

Anthropic describes compaction, structured note-taking, and focused retrieval as ways to manage long tasks. Our application here is to preserve decisions and evidence references while allowing detailed history to remain outside the active prompt. [Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## Memory that can be corrected

Every durable claim needs an ID, source, scope, review date, and status. Distinguish “the user prefers X” from “a benchmark suggests X.” When a claim changes, mark the old record superseded and preserve why. At resume, check the actual worktree and running processes before trusting a handoff.

Supermemory authentication and reachability have been verified; storage receipts are tracked separately. The [memory directory](../memory/README.md) contains portable records; it is not evidence of a successful remote write. A working integration must demonstrate write, retrieval in a fresh context, correction, and deletion.


Next: [Coding workflow](04-coding-workflow.md).
