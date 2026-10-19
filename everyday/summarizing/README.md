# Summarize evidence without promoting proposals into decisions

[Everyday examples](../README.md) · [Prompt fundamentals](../../handbook/01-first-example.md)

A volunteer missed the meeting. They need the final decisions and next actions, not a fluent paragraph that mixes settled and unsettled items.

The request defines three categories and asks for line references. The references make it easier to inspect support, but a citation is useful only if the cited line actually supports the statement.

## Supplied material

```text
Fictional neighborhood library meeting notes:
[L1] The group approved a Saturday reading club starting 2027-03-06, from 14:00 to 15:00.
[L2] Jordan accepted responsibility for reserving the room by 2027-02-25.
[L3] Priya suggested buying 20 new books. No budget or purchase was approved.
[L4] Accessibility requests should go to the library desk. The group has not chosen a contact person.
[L5] The earlier proposed 13:00 start time was explicitly replaced by the approved 14:00 start.
[L6] Attendance capacity and registration details remain undecided.
```

## Exact request

```text
Summarize the supplied library meeting notes for a volunteer who missed the meeting. Use three short sections: Confirmed decisions, Actions, and Still undecided. Add the supporting line IDs to each factual bullet. Separate proposals from approvals, preserve the final start time, and do not invent an owner, capacity, budget, or registration process. Use only these notes. Do not use tools.
```

## Recorded response

The following is the actual saved model output, with no content edits:

> ### Confirmed decisions
> - Saturday reading club starts 2027-03-06, 14:00–15:00. The approved 14:00 start replaces the proposed 13:00 start. [L1, L5]
>
> ### Actions
> - Jordan will reserve the room by 2027-02-25. [L2]
> - Send accessibility requests to the library desk; no contact person has been chosen. [L4]
>
> ### Still undecided
> - Priya proposed buying 20 new books; no purchase or budget was approved. [L3]
> - Attendance capacity and registration details remain undecided. [L6]

[Raw response](response.txt) · [Complete assembled request](request.txt) · [Execution log](execution.log)

## Check the result

| Check | Recorded response |
|---|---|
| Final start time | Uses 14:00 and notes it replaced 13:00, citing L1 and L5 |
| Confirmed owner and deadline | Names Jordan and 2027-02-25, citing L2 |
| Book purchase | Retains it as a proposal with no approved budget or purchase, citing L3 |
| Accessibility | Gives the library desk and preserves the missing named contact, citing L4 |
| Remaining gaps | Keeps capacity and registration undecided, citing L6 |

All factual bullets have supporting line references. The authoring assistant compared each to the source notes; no independent human annotation was collected.

## A failure to watch for

A summary could incorrectly announce “Priya will buy 20 books” or give the old 13:00 start time. The first changes a proposal into an assigned action; the second ignores the explicit replacement.

Use the same pattern for your documents: decide which distinctions matter, ask for evidence references, and inspect a sample of claims. For a high-consequence summary, check all material claims rather than relying on its confident tone.
