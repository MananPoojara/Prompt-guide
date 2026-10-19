# 1. Your first complete example

[Start](../START-HERE.md) · Next: [What the model receives](02-model-and-context.md)

A prompt is the input you provide to ask a model to do something. In a chat interface, it may look like one message. In a coding agent, the request reaching the model can include that message, application instructions, selected files, available tools, and previous tool results. Start with one message so you can see the pieces.

## A task with an answer you can check

These are the complete fictional notes used in our saved comparison:

```text
- Search fix: Priya will do it by 2026-11-03.
- Export fix: no owner assigned; deadline not decided.
- Dashboard: Alex proposed 2026-11-05. No one accepted ownership or a deadline.
- Login bug: Sam owns it. The deadline was 2026-11-04, then explicitly changed to 2026-11-06.
```

The job is to extract the task, owner, and deadline. “Extract” means take the information from the notes, not make sensible project-management decisions on the team's behalf. Priya is assigned. Alex is mentioned, but not assigned. Sam's later deadline replaces the earlier one.

Here is the complete shorter prompt, before the notes are appended:

```text
Extract the owner and deadline for each task in the notes below. Return only a JSON array with one object per task, using keys task, owner, deadline.
```

JSON is a text format programs can read. An array is an ordered list inside square brackets. An object groups named fields inside braces. In this example, `null` means no confirmed value; it does not mean the word “null” appeared in the notes. A person reading a chat answer might accept a paragraph, but a program importing tasks may require exactly these fields.

The expected answer is:

```json
[
  {"task": "Search fix", "owner": "Priya", "deadline": "2026-11-03"},
  {"task": "Export fix", "owner": null, "deadline": null},
  {"task": "Dashboard", "owner": null, "deadline": null},
  {"task": "Login bug", "owner": "Sam", "deadline": "2026-11-06"}
]
```

## Make the decision rules visible

The longer prompt makes the ambiguous cases explicit:

```text
Extract confirmed task ownership and deadlines from the notes below. Return only a JSON array with one object per task, preserving task order, using exactly keys task, owner, deadline. Use a person's name only when ownership is explicitly assigned. Use an ISO date only for an explicitly confirmed deadline. Unassigned, undecided, and merely proposed values must be JSON null. An explicitly changed deadline supersedes the previous deadline. Do not infer commitments.
```

“Confirmed” establishes the boundary between a proposal and a commitment. The `null` instruction tells the model how to represent missing information. The supersession rule tells it which of two dates to keep. These are decisions the task owner can explain and a checker can inspect.

Both prompts receive identical notes. The longer wording is our authored candidate, not a secret prompt from an AI laboratory. You can open the complete [baseline](../labs/prompt-contract/baseline.txt), [candidate](../labs/prompt-contract/candidate.txt), and [expected answer](../labs/prompt-contract/expected.json).

## What actually happened?

Both prompts produced the expected extraction for all four tasks in the recorded run. That is **4/4 versus 4/4**, one response per prompt. The saved [baseline output](../labs/prompt-contract/results/baseline.txt) and [candidate output](../labs/prompt-contract/results/candidate.txt) let you inspect the result directly. The [run report](../labs/prompt-contract/RESULTS.md) identifies the model and procedure.

This matters because a tutorial can easily show a made-up bad answer, replace the prompt, and imply the replacement caused an improvement. Here the shorter prompt already worked. The longer prompt documents the intended policy more clearly, but this run provides no observed accuracy advantage.

The grader reads the outputs as JSON and compares their contents with the expected values. Run it without an AI account:

```bash
python3 labs/prompt-contract/grade.py
```

It rechecks saved responses. It does not ask a model for fresh responses.

## Apply the pattern to your own task

Start with the decision you need the output to support. For a task importer, incorrect ownership may matter more than elegant prose. For a research summary, separating a source's statement from your inference may matter more than a rigid JSON shape.

A useful request contains a task, the relevant material, the important decision rules, and the desired output. Add an example when a rule is hard to describe. Give an explicit behavior for missing information when guessing would be harmful. Add constraints because the task needs them, not because a long prompt looks sophisticated.

For example, “summarize this meeting” can be sufficient when you want an informal overview. If you intend to assign work automatically, define what counts as an assignment first. The necessary precision comes from the consequences of the output.

If you try the prompt in your own chat application, its model, settings, conversation history, and application instructions may differ. Keep your result as a new observation. Reproducing the wording is only one part of reproducing the system.
