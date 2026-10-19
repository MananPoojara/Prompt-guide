# Research and build flow

## Objective

Create a public, practical prompting guide at `MananPoojara/Prompt-guide` with actual prompts, explanations, diagrams, reproducible before/after examples, and source-backed research. Preserve findings in Supermemory. Teach public engineering practices without claiming private lab access.

## Method and decisions

1. Read the original brief and inspect the empty repository.
2. Retrieve primary documentation, engineering articles, and research abstracts. Track what each source supports and its limits in research/sources.md.
3. Build a learning path: specification, model behavior, context, coding, tools, harnesses, evaluation, and ongoing research.
4. Write original task-specific prompts with acceptance checks and failure modes.
5. Execute a prompt comparison and a separate coding demonstration. Preserve raw outputs and report ties honestly.
6. Check the artifacts, save focused research memories, and publish to the requested GitHub repository.

Markdown makes lessons directly readable on GitHub. The four-field prompt contract is an original teaching framework, not a claimed internal lab standard. Illustrations and executed results are explicitly distinguished. Historical papers establish scoped results; no modern-model universality is claimed. Unknown terms and unverified internal-workflow stories remain unresolved in research/claims.md.

## Research access

Source review date: 2026-10-19. Official OpenAI documentation tools and web retrieval supplied the primary-source research. Exa encountered a certificate-chain error. Twitter and Reddit backends were unavailable; no private posts or unattributed social claims were used as evidence. Agent Reach's update check reported the installed v1.5.0 current.

## Delivered artifacts and evidence

| Requirement | Artifact | Verification |
|---|---|---|
| Deep, practical learning path | Eight guides in guides/ | Each has concrete examples, exercises, and scoped claims |
| Prompts inside the repo | Twelve templates in prompts/ | Copyable text, use case, result check, failure mode |
| Research provenance | research/sources.md and research/claims.md | Fifteen primary sources; review dates and limitations |
| Images and diagrams | diagrams/learning-loop.svg; harness Mermaid graph | SVG parsed, rendered, and visually inspected |
| Real prompt outputs | labs/prompt-contract/ | Both observed outputs match 4/4 records; one attempt each, a tie |
| Real coding before/after | labs/search-fix/ | 3/5 tests failed before; 5/5 passed after; tests byte-identical |
| Honest evaluation | Lab READMEs and RESULTS.md | Limits and confounds stated; no superiority claim |
| Maintainability | CONTRIBUTING.md; GitHub Actions workflow | Offline link, grader, and saved-code checks configured |
| Memory management | memory/ | Focused local records; remote receipts tracked in memory/README.md |
| Public publication | Requested GitHub origin | Initial commit 2f501b6 verified on origin/main; GitHub Actions run 39208827349 passed |

## Checks performed

- All local Markdown link targets exist; external links and anchors are outside this checker's scope.
- Six grader tests passed, including rejection of malformed, missing, extra, and incorrect data.
- Extraction outputs both scored 4/4 with complete exact-output matches.
- Independent search test execution passed all five checks after the change.
- SVG parsed and rendered successfully, with readable labels and arrows.
- Credential-pattern scan found no API-key-shaped strings in repository files.
- Staged diff whitespace check passed.

## Supermemory

Browser OAuth succeeded. Direct API and hosted MCP identity checks succeeded with `NODE_USE_SYSTEM_CA=1`; this uses trusted system certificates without disabling TLS verification. Three focused records were accepted in the server's default namespace `sm_project_default`. Search initially returned no results while ingestion was queued. All three reached done and complete contents were retrieved via get_document; see memory/receipts.json. Semantic-search recall is not claimed. The configured automatic recall project container differs from this hosted default, so automatic recall is not assumed.

This file records decisions, evidence, and next actions; it is not a private internal reasoning transcript. Future research and new examples are ongoing maintenance, not evidence that these initial experiments generalize.

## Publication verification

Published to [MananPoojara/Prompt-guide](https://github.com/MananPoojara/Prompt-guide). The initial content commit passed [GitHub Actions](https://github.com/MananPoojara/Prompt-guide/actions/runs/39208827349). Remote branch hash matched the local content commit. This final documentation update records the completed memory readbacks and publication evidence.

## User-directed revision: resource, not coursework

The user clarified that the value must be inspectable real engineering: original prompts, documented use, diagrams, and observed behavior across model inputs, skills, plugins, MCP, harnesses, loops, and graphs. The first lesson-led edition did not satisfy that emphasis. The current front page leads with source artifacts and cases; authored templates remain separately labeled, and exercise paragraphs were removed.

### What changed

- Six original prompt artifacts from three publisher-owned repositories are preserved with pinned revisions, SHA-256 hashes, and licenses. Notebook strings are exact extracted values; full-file snapshots are byte-preserved.
- A named Anthropic Labs engineer's reported experiment includes his exact short task prompt, a sourced workflow diagram, and limits on causal interpretation.
- The autonomous-coding quickstart's conflicting license statements are documented; its complete prompt files are linked rather than copied under an assumption.
- Anthropic's unchanged evaluator prompt was run six times in Codex across two fixtures, alternating order. The defective fixture was rejected three times; the behaviorally repaired fixture accepted three times. Its amortized-versus-worst-case ambiguity is retained as a limitation.
- Actual evaluator feedback was supplied to Anthropic's unchanged generator prompt. The generated revision passed independent behavior checks and a fresh evaluation. Inputs, outputs, logs, generated code, and checks are saved.
- Eight case checks and six existing grader checks pass. Original snapshot integrity checks pass. The new diagram was rendered and visually inspected.
- X launch copy and a proposed one-day editorial/validation schedule are saved under launch/. They are drafts, not posted content or a claim that a day has elapsed. A fresh Agent Reach check found no active X backend.

The local reproduction uses Codex, not the upstream Claude API configuration. It does not establish universal prompt effectiveness, private employee routines, or superiority over a no-feedback control. The resource makes those boundaries visible next to the examples.
