# Rewrite an email without changing its promises

[Everyday examples](../README.md) · [Prompt fundamentals](../../handbook/01-first-example.md)

You want the message to sound warmer and be easier to act on. The important boundary is factual: a nicer rewrite must not promise a refund or a replacement date that the organizer never offered.

The request names the audience, asks for a subject line, limits length, and explicitly protects the scheduling details. Those constraints come from the task, not from a universal rule that every email needs a long prompt.

## Supplied material

```text
Fictional message from a community workshop organizer:
"Hi. Saturday's pottery workshop is moved from 10:00 to 11:30 because the room needs repairs. Same building, room 4 instead of room 2. If this doesn't work, reply by Thursday 18:00 and we can move your booking to another session. We can't confirm which session yet. Sorry about this."
```

## Exact request

```text
Rewrite the supplied workshop message as a warm, concise email to attendees. Include a subject line and keep the body under 110 words. Preserve every logistical detail and the Thursday response deadline. Make the requested action easy to spot. Do not invent a refund policy, promise a replacement date, or imply that another session is already confirmed. Use only the supplied message. Do not use tools.
```

## Recorded response

The following is the actual saved model output, with no content edits:

> Subject: Saturday’s pottery workshop: new time and room
>
> Hi everyone,
>
> Sorry for the change: Saturday’s pottery workshop will start at 11:30 instead of 10:00 because the room needs repairs. We’ll be in the same building, in room 4 instead of room 2.
>
> **If this doesn’t work for you, please reply by Thursday at 18:00.** We can move your booking to another session, but we can’t confirm which session yet.
>
> Thank you for your understanding.

[Raw response](response.txt) · [Complete assembled request](request.txt) · [Execution log](execution.log)

## Check the result

| Check | Recorded response |
|---|---|
| New time and old time | Preserves 11:30 instead of 10:00 |
| Location | Preserves the same building and room 4 instead of room 2 |
| Reason | Says the room needs repairs |
| Action and deadline | Clearly asks affected attendees to reply by Thursday at 18:00 |
| Uncertainty | Says the replacement session cannot yet be confirmed |
| Unsupported promises | Adds no refund policy or confirmed replacement date |

The body is under the requested 110-word limit. This is a manual content review by the authoring assistant, not a measured score for warmth or readability.

## A failure to watch for

A rewrite might say “Your refund is guaranteed” or “We have reserved a place next Saturday.” Either sentence would invent a commitment. Even polished writing needs a factual comparison against the original.

When adapting this request, specify which facts must survive the rewrite. If a detail is unclear, ask the assistant to flag it rather than fill it in.
