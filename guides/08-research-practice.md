# 8. Learn from labs without inventing their private workflows

A public engineering post can tell you how a team approached a specific problem. It does not expose every internal prompt, repository, or decision. Keep the scope of your conclusion matched to the evidence.

## What “models evaluate models” can mean

Models can generate test scenarios, act as simulated users, inspect transcripts, or grade specified behavior. These are distinct roles. Anthropic's Bloom describes a configurable behavioral evaluation pipeline and checks agreement with human judgments. It does not establish that a model independently certifies its own correctness. [Bloom](https://www.anthropic.com/research/bloom)

Anthropic's Automated Weak-to-Strong Researcher describes agents proposing ideas, running experiments, and iterating on a bounded research problem. Its discussion highlights evaluation design and overfitting as bottlenecks. That is evidence of a particular research system, not proof that a generic self-improvement prompt recreates it. [Research report](https://alignment.anthropic.com/2026/automated-w2s-researcher/)

## A source-checking workflow

```text
Investigate this claim: [exact claim]. Find the original publication, dated
product documentation, or repository. Open the source and identify what it
actually establishes. Separate observations, authors' interpretations, and
your inference. Identify task, model, evaluation method, and limitations.
If the source is missing, label the claim unverified. Propose a small local
experiment only when it would test a relevant implication.
```

An unknown term such as “harness2” or “jev” needs an exact source before we define it. A viral post is a discovery lead; it is not enough to attribute an internal workflow to a lab. The claim that these teams universally use Obsidian is unverified in this research pass.

## Updating the repository

When a new release or article appears, ask which existing lesson or prompt it changes. Record the old claim, new evidence, affected files, and whether rerunning a lab is necessary. Keep conceptual lessons stable when only a product name changes. Do not silently rewrite old experiment metadata to match a new model.

Suggested cadence: review product instructions monthly and conceptual sources when new evidence contradicts them. This is a maintainer procedure, not an installed background automation. Use [the contribution checklist](../CONTRIBUTING.md).

**Exercise:** take a new AI claim and write two sentences: the strongest statement the evidence supports, and one tempting overclaim it does not support. Add the source and review date.

Return to the [learning path](../README.md) or choose a [prompt](../prompts/README.md).
