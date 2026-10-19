# Useful skills, plugins, and MCP servers

[Back to Prompt Guide](../README.md) · [How skills work](../handbook/05-skills-and-plugins.md) · [How MCP works](../handbook/06-tools-and-mcp.md)

Start with a task you already have, then choose one addition that helps with it. This is a small editorial shortlist selected for a clear purpose, identifiable maintainers, and inspectable documentation. It is not a popularity ranking or a benchmark of the best tools.

**Checked: 2026-10-19.** These external projects were source/documentation-inspected for this list, not installed or executed as part of the review. [Inspection records](sources.json) retain repository revisions. Our separately [executed local MCP example](../examples/mcp-notes/README.md) remains the simplest way to learn the protocol without a model account.

## Pick by the job

| Your task | Starting point | Kind | Why it belongs here |
|---|---|---|---|
| Work with PDFs, slides, spreadsheets, or documents | [Anthropic skills](https://github.com/anthropics/skills) | Skills, available in plugin bundles | Concrete examples of reusable task procedures |
| Review a GitHub pull request | [Anthropic code-review plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review) | Claude Code plugin | Shows a packaged review workflow with multiple reviewers |
| Inspect and interact with a web application | [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) | MCP server | Gives a compatible agent browser operations |
| Look up documentation for a library | [Upstash Context7](https://github.com/upstash/context7) | MCP or CLI + skill | Retrieves library documentation into the agent's context |
| Read repository, issue, or PR information | [GitHub MCP Server](https://github.com/github/github-mcp-server) | MCP server | Connects a compatible host to GitHub operations |

A **skill** supplies a procedure. A **plugin** packages capabilities for a host. An **MCP server** exposes operations through a protocol. One project can offer more than one delivery method.

## 1. Anthropic skills: document workflows

The repository contains individual skill folders with instructions and supporting resources. Its document examples cover PDF, DOCX, PPTX, and XLSX work. Use them to study how a broad task is broken into concrete operations and checks.

For Claude Code, the upstream README gives this setup:

```text
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**First task to try — our example prompt:**

```text
Use the PDF skill to extract the headings and page numbers from this sample PDF.
List pages you could not read. Preserve the original file.
```

**Check the result:** compare several headings and page numbers against the actual PDF, including a page with unusual formatting. Successful skill loading does not establish extraction accuracy.

**Compatibility and reuse:** the installation above is for Claude Code; other hosts have their own loading rules. The repository distinguishes open-source examples from source-available document skills. Check the individual skill's license before copying or redistributing it. [Source and installation](https://github.com/anthropics/skills).

## 2. Code-review plugin: a packaged review process

This Anthropic-maintained plugin describes a pull-request review workflow involving multiple reviewers, repository instructions, and filtering of findings. It is a useful concrete example of a plugin coordinating a workflow rather than merely changing response style.

In Claude Code, find `code-review` in `/plugin` → Discover, or use the directory's documented install pattern:

```text
/plugin install code-review@claude-plugins-official
```

**First task:** use a disposable PR with one known defect and examine whether the findings identify it and cite the correct lines. This is a proposed trial, not a result we measured.

**Requirements and effects:** the plugin documents GitHub CLI access and authentication. Its workflow can post review comments; inspect the current command instructions before invoking it on a shared PR. Model usage depends on your runtime. A generated confidence score is not a measured probability of correctness.

Read the [plugin README and command files](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-review). The [marketplace README](https://github.com/anthropics/claude-plugins-official) distinguishes Anthropic-maintained plugins from external entries; listing in the same directory does not make every plugin Anthropic-authored.

## 3. Playwright MCP: browser interaction

Playwright MCP exposes browser automation, including interaction through structured accessibility information. It is useful when an agent needs to inspect and operate a page rather than reason from source code alone.

The upstream README supplies client-specific setup and a standard server configuration using `npx` and `@playwright/mcp`. It lists Node.js 18+ and a compatible MCP client as prerequisites. Follow the configuration for your actual host.

**First task to try — our example prompt:**

```text
Open my local demo page. Search for "tea" and report the visible results.
Describe the steps you performed and any browser errors. Do not submit purchases.
```

**Check the result:** inspect the page yourself and compare the reported results with the visible UI. Use a local demo or test account for the first run.

**Alternative:** Microsoft's README also points coding-agent users toward its CLI + skills option. MCP is one integration choice, not a requirement for browser automation. Compare the fit to your host and workflow. [Setup and comparison](https://github.com/microsoft/playwright-mcp).

## 4. Context7: library documentation in context

Context7 offers documentation retrieval through either MCP or a CLI with skills. It can help when a coding task depends on a specific library API. Request the library and version explicitly, then inspect the returned source before adopting the code.

**Setup:** the upstream README describes `npx ctx7 setup`, which authenticates and configures a chosen integration. It currently lists Node.js 22.13+ for that CLI and recommends an API key for higher limits. Setup changes agent configuration; choose the intended host and mode. [Setup and client-specific instructions](https://github.com/upstash/context7).

**First task to try — our example prompt:**

```text
Use Context7 to find the documentation for the version of this library in my
package file. Show the relevant API signature and source before suggesting a change.
If that version is unavailable, say so.
```

**Check the result:** verify the selected package/version and run the relevant code check. Retrieved documentation can improve the available evidence; it does not guarantee correct generated code. Documentation queries go to the selected service, so keep them focused on the public API you need.

**When documentation helps, source-checked 2026-10-19:** porting code between libraries, platforms, or SQL dialects can depend on API details just as new implementation does. Do not exclude a task merely because it is called refactoring or code review; ask whether correct behavior depends on an external API. Pure internal logic or general concepts may not need a documentation lookup. This reflects the [narrowed upstream rule](https://github.com/upstash/context7/blob/5a2b65145b5930d2773e79d3a223fa5fb2b308ad/rules/context7-mcp.md), inspected as source, not executed as a new integration. Existing host configuration may retain an older rule.

**Error handling, source-checked 2026-10-19:** Context7 MCP 4.4.3 marks a failed library-resolution search with `isError: true`; an empty successful search remains a normal result. Preserve that distinction in your host. See the [reviewed update](../updates/2026-10-19-context7-errors.md) for the pinned source and execution limits.

## 5. GitHub MCP Server: repository context and actions

GitHub's server exposes repository, issue, pull-request, and other GitHub operations. Its README describes hosted and local routes, host-specific setup, authentication, and configurable tool access.

**First task to try — our example prompt:**

```text
Read this PR's description, changed files, and check results. Summarize its purpose
and any failing checks, with links. Do not comment, edit, merge, or close anything.
```

**Check the result:** compare the summary with the PR and CI pages. Start with the documented read-only configuration and access appropriate to the target repository. A prompt asking for read-only behavior is separate from restricting the server's available operations.

Use the [official installation instructions](https://github.com/github/github-mcp-server), selecting the section for your host. If your existing GitHub CLI workflow already meets the task, you may not need another integration.

## Decide whether to keep an addition

Try one representative task and inspect the output. Record the host, tool version, setup, and failure cases. Keep the addition if it supplies a capability or repeatable procedure you actually use. Remove overlapping or unused integrations instead of loading everything you find.

To suggest an addition here, provide its primary repository, a concrete use case, supported host/setup, relevant permissions or external effects, and a small check a reader can perform. See [contributing](../CONTRIBUTING.md). Prefer a few well-explained entries over a directory of unexplained links.
