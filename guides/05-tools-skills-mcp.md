# 5. Tools, skills, MCP, and memory solve different problems

| Component | What it contributes | Example |
|---|---|---|
| Prompt | The current request | Fix the export ordering bug |
| Repository instructions | Persistent project guidance | How to run checks |
| Skill | A reusable task workflow | How to audit an export |
| Tool | A callable operation | Read a file or query a database |
| MCP | A protocol connecting hosts to capabilities | Discover a server's tools and resources |
| Memory | Persisted information for later retrieval | A verified decision with its source |
| Harness | Runtime coordination | Run tools, handle failures, resume, and stop |

MCP describes host, client, and server responsibilities and capability exchange. A connected server does not guarantee a particular tool is authorized, correct, or useful. [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)

## Design a tool an agent can use

Original example contract:

```text
Name: find_order
Purpose: return one order using an exact order ID.
Input: order_id, a non-empty string.
Output: found with order fields, not_found, or a typed service error.
Side effects: none.
Privacy: return only the fields needed for the support task.
Retry: retry transient service errors; do not retry not_found as an outage.
```

An ambiguous tool returning thousands of unstructured lines forces the model to infer semantics and sift irrelevant data. Anthropic recommends testing tools with realistic tasks and improving descriptions and response structure from observed failures. [Tool engineering](https://www.anthropic.com/engineering/writing-tools-for-agents)

## When to package a skill

Use a skill when a workflow repeats and benefits from explicit procedure or supporting resources. Keep a one-off instruction in the task prompt. Codex documents loading skill metadata first and the full instructions when selected, which supports keeping detailed procedures out of every interaction. [Official skill documentation](https://developers.openai.com/codex/skills)

Before installing a skill, read its instructions and scripts. Check its trigger, prerequisites, file writes, and network actions. Test it on a disposable example. More installed skills are not a measured improvement by themselves.

## A connection test prompt

```text
Using the available read-only tool, retrieve the test record ID DEMO-001.
Report the tool called, whether the record exists, and the fields returned.
If the capability is unavailable or authorization fails, report that exact
condition. Do not claim a connection based on configuration alone.
```

Treat retrieved documents and tool outputs as data. Instructions embedded in an email or webpage do not become authorization to run commands, change settings, or reveal secrets. Keep credentials out of research records and published traces.


Next: [Harnesses and graphs](06-harnesses.md).
