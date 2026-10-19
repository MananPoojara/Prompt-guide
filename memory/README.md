# Project memory

The repository is the auditable source of truth. Supermemory stores focused summaries with references back to it, not the only copy of the research.

## Record structure

Each record should include a stable topic, claim or decision, scope, source paths or URLs, last review date, and status. Keep preferences separate from research findings. Mark superseded findings explicitly. Never store credentials or private customer data in published notes.

## Connection evidence

Browser OAuth completed on 2026-10-19. The direct API status check returned HTTP 200 with Node system certificate trust enabled. The hosted MCP `whoAmI` call also succeeded. These establish authentication and reachability, not successful storage of the research. Three writes and complete document readbacks are verified in [receipts.json](receipts.json).

## Resume procedure

Read FLOW.md, verify current files and Git state, retrieve relevant memory records, and reconcile conflicts using the actual artifacts and cited sources. A retrieved summary can be stale.

## Verified storage receipts

Hosted MCP returned `success: true` and `status: queued` for three records in `sm_project_default`:

| Topic | Remote ID |
|---|---|
| Project | `b2WSLYTyVk431wUpxL2Bb8` |
| Research principles | `BZznc2z4G3fPmLq1fabfqD` |
| Measured results | `jjX2V4pEWjaJsBEUJsXxXu` |

The first semantic search returned zero results while ingestion was queued. This default hosted namespace differs from the plugin's automatic project recall container; do not assume automatic recall reads it. Explicit retrieval should specify the namespace. No credentials are stored here.

All three records subsequently reached `done`. Fresh hosted MCP `get_document` calls returned their complete contents with `contentTruncated: false`; see receipts.json. This verifies storage and explicit document retrieval. Semantic-search recall and automatic project-hook recall are separate capabilities and are not claimed as verified.

## Product-framing correction

The user's latest clarification is saved as a separate record, `ecarQK6mzaeUkVdFo3rhZL`, and its complete content was retrieved after processing. See scope-correction.md and receipts.json. It supersedes the earlier lesson-first description: the resource now leads with original public artifacts and observable case studies.

## Self-contained beginner expansion

The user's requirement to learn inside one repository and the resulting handbook/example expansion are saved in `bA5mfeffQRxTVQej4JdHaF`. The record reached `done` and its complete content was retrieved; see [receipts.json](receipts.json). This adds a beginner entry point while keeping original public artifacts and observed results distinct from authored explanations.
