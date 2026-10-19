# X launch draft

Audience: people building software with AI assistants. Goal: help readers inspect real examples and reuse them with their prerequisites understood. Draft only; not posted.

## Main post

I’m building Prompt Guide: original public prompts from Anthropic and OpenAI, with the context, tools, and workflows around them.

A beginner handbook explains the concepts inside the repo, with diagrams, actual outputs, and a local MCP demo.

A few examples ↓

## Reply 1

The interesting part is often outside the chat box.

One Anthropic engineer published a one-sentence game-maker prompt. His comparison changed the surrounding workflow: planning, building, browser testing, and feedback.

The case links the original report.

## Reply 2

We also ran Anthropic’s published evaluator prompt in Codex on two small code fixtures.

All three attempts rejected a duplicate-minimum bug. All three accepted the repaired fixture—but the feedback exposed an ambiguity about O(1) complexity.

The outputs are saved.

## Reply 3

The resource separates:

• Original published prompts
• Authors’ reported experiments
• Our local reproductions
• Our own explanations and adaptations

No claim of access to private lab prompts. No hiding ties or failures.

## Reply 4

Browse the prompts, workflow diagrams, and recorded cases:

https://github.com/MananPoojara/Prompt-guide

If you have a primary-source prompt with a real workflow behind it, send the source. That’s the kind of contribution this needs.
