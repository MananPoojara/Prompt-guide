# Make a plan that fits the time you actually have

[Everyday examples](../README.md) · [Clarify before planning](clarification.md)

A useful schedule respects the time window, dependencies, and breaks. Asking for an “efficient plan” alone does not tell the model what it may change. Here, the supplied durations are fixed, and the buffer must stay unused.

## Supplied facts

```text
Fictional task: prepare eight paper-craft kits on Saturday, from 10:00 to 11:30.
Required work and fixed estimates:
- Sort materials: 20 minutes, before packing.
- Pack all kits: 25 minutes, after sorting and before labeling.
- Label kits: 15 minutes, after packing.
- Clean the workspace: 10 minutes, after packing and labeling.
- Take a fixed break from 10:45 to 10:55.
- Keep the final 10 minutes, 11:20 to 11:30, as an unused buffer.
Optional: make an inventory spreadsheet, estimated at 20 minutes.
Only one person is working; tasks cannot overlap. Use the supplied estimates without shortening them.
```

## Exact request

```text
Make a usable schedule from the supplied facts. Return a simple table with start time, end time, and activity. Respect dependencies, the fixed break, and the final unused buffer. State which optional work does not fit and why. Check that the minutes add up to the available window. If the required work cannot fit, explain the conflict instead of inventing a shorter duration. Do not use tools.
```

## Recorded response

Actual saved response, with no content edits:

> | Start time | End time | Activity |
> |---|---|---|
> | 10:00 | 10:20 | Sort materials |
> | 10:20 | 10:45 | Pack all eight kits |
> | 10:45 | 10:55 | Fixed break |
> | 10:55 | 11:10 | Label kits |
> | 11:10 | 11:20 | Clean the workspace |
> | 11:20 | 11:30 | Unused buffer |
>
> The optional inventory spreadsheet does not fit: it needs 20 minutes, and no time remains outside the fixed break and unused buffer.
>
> Minute check: 20 + 25 + 10 + 15 + 10 + 10 = **90 minutes**, matching the 10:00–11:30 window. All dependencies are respected, with no overlapping tasks.

## Check it yourself

| Constraint | Observed check |
|---|---|
| Required work uses its full estimates | Sorting 20 + packing 25 + labeling 15 + cleaning 10 =70 minutes |
| Fixed break | 10:45–10:55, exactly 10 minutes |
| Final buffer remains free | 11:20–11:30, exactly 10 minutes |
| Available window | 70 work +10 break +10 buffer =90 minutes |
| Dependencies | Sorting precedes packing; packing precedes labeling; cleanup follows both |
| No overlap or gaps | Each block ends when the next begins |
| Optional task | Spreadsheet explicitly omitted because its additional 20 minutes do not fit |

These checks were performed by the authoring assistant against the supplied constraints. They are not independent human review or a real-world timing study. The estimates are fictional inputs; the example does not establish how long preparing kits would actually take.

## A failure to recognize

**Authored failure illustration, not a model output:** “Use 11:20–11:30 for the spreadsheet.” That consumes the reserved buffer and gives a 20-minute task only 10 minutes. A tidy table would not make that plan feasible.

Before using a plan, check totals and dependencies yourself. If the required tasks exceed the window, ask the model to expose the conflict and identify what must change—scope, duration, resources, or deadline. Do not accept silently shortened estimates as an optimization.

## Adapt the request

Replace the tasks, estimates, fixed appointments, and dependencies with your own. Mark estimates as uncertain if they are uncertain; include the reserve you need. Make clear which tasks are optional and which constraints may be negotiated.

The [recording notes](README.md) contain provenance, reproduction commands, and limitations. This is one successful demonstration, not evidence that this prompt outperforms another.
