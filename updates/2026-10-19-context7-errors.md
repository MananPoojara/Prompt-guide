# 2026-10-19 — Distinguish a failed documentation lookup from no matches

**For:** developers integrating Context7's MCP tools.

The first source-watch collection detected two commits after our inspected Context7 revision. Source review found that MCP package 4.4.3 marks a failed `resolve-library-id` search with `isError: true`; a completed search with no matching libraries remains a normal result. Your host should preserve that distinction: an unavailable lookup is not evidence that a library does not exist. This is useful error handling even when the returned text sounds similar.

The [toolkit guidance](../toolkit/README.md) now calls out that check. Its beginner setup instructions are unchanged by this diff. We inspected the changelog and relevant source changes; we did not install this release or execute its error path. The update makes no measured performance claim.

**Source:** [upstream comparison](https://github.com/upstash/context7/compare/6b636d3c35e051a1a653a236afb7f612c02a1ad3...ae4871e9a8cbed00bc0f4a40b0b5b61e2d37378c), specifically `packages/mcp/CHANGELOG.md` and `packages/mcp/src/index.ts`. Checked 2026-10-19. The source ledger retains the previous revision and the scope of this incremental review.

**Action:** when integrating, test both an upstream failure and an empty successful search in your host. Do not label a transport/service failure “no documentation found.” This proposed host test was not performed here.
