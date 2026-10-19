# Project memory

The repository is the auditable source of truth. Supermemory stores focused summaries with references back to it, not the only copy of the research.

## Record structure

Each record should include a stable topic, claim or decision, scope, source paths or URLs, last review date, and status. Keep preferences separate from research findings. Mark superseded findings explicitly. Never store credentials or private customer data in published notes.

## Connection evidence

Browser OAuth completed on 2026-10-19. The direct API status check returned HTTP 200 with Node system certificate trust enabled. The hosted MCP `whoAmI` call also succeeded. These establish authentication and reachability, not successful storage of the research. Write and retrieval receipts will be recorded after those operations succeed.

## Resume procedure

Read FLOW.md, verify current files and Git state, retrieve relevant memory records, and reconcile conflicts using the actual artifacts and cited sources. A retrieved summary can be stale.

## Accepted write receipts

Hosted MCP returned `success: true` and `status: queued` for three records in `sm_project_default`:

| Topic | Remote ID |
|---|---|
| Project | `b2WSLYTyVk431wUpxL2Bb8` |
| Research principles | `BZznc2z4G3fPmLq1fabfqD` |
| Measured results | `jjX2V4pEWjaJsBEUJsXxXu` |

The first semantic search returned zero results while ingestion was queued. This default hosted namespace differs from the plugin's automatic project recall container; do not assume automatic recall reads it. Explicit retrieval should specify the namespace. No credentials are stored here.
