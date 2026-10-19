# Readiness audit: delivered evidence and unfinished requirements

[Core checklist](../CORE-COVERAGE.md) · [Roadmap](../ROADMAP.md) · [Reader review](README.md)

**Disposition: not yet ready to declare the full maintenance milestone complete.** This audit inspects the roadmap and evidence at base commit `d58d6f2e65046301b5eecb9e761972831c4ad7f4`, with the accompanying mobile-table correction. It does not redefine readiness as whatever currently passes tests. It preserves the missing noncoding research/revision example, independent review, actual judge calibration, and sustained maintenance evidence as open work.

## Evidence by requirement

| Requirement from the goal or roadmap | Inspected evidence and what it establishes | Status / limit |
|---|---|---|
| Beginner entry without accounts | [Start Here](../START-HERE.md), [first complete example](../handbook/01-first-example.md), and [five everyday cases](../everyday/README.md) supply local inputs, requests, responses, and checks | Initial path delivered; actual beginner comprehension unverified |
| Writer/student/researcher path | Roadmap explicitly promises source-grounded research and revision, including fabricated claims and citation failures | **Incomplete:** technical grounding labs and email rewriting do not replace a complete noncoding research/revision case |
| Visual model mechanics | [Token/sampling recording](../labs/model-mechanics/README.md), [representations](../labs/representations/README.md), and [context budgets](../labs/context-budget/README.md) | Measured small-model demonstrations delivered; no proprietary-model interpretation or learning-outcome claim |
| Usable local visuals | Both existing Playwright scripts passed in this audit; [targeted visual record](visual-audit-2026-10-19.json) checks caption bounds and keyboard scrolling after the fix | Tested Chromium controls/layout, no external requests, and narrow widths; no screen-reader study or accessibility certification |
| Public original prompts | [Originals manifest and licenses](../originals/README.md); source checker verifies exact files and notebook string extraction | Published artifacts verified locally; private engineer workflows and current defaults not established |
| Prompt comparisons | [Extraction pilot](../labs/prompt-comparison/README.md), [natural notes](../labs/natural-notes/README.md), and [examples/decomposition](../labs/example-design/README.md) retain all conditions and ties | Initial comparisons delivered; independent annotations and harder independent tests remain open |
| Realistic retrieval and evidence | [Real-document lab](../labs/real-docs/README.md) retains six official historical spec pages, source spans, embeddings, ranks, packing, and twelve answers | Initial real-document pipeline delivered; source/rank/scoring checks are not independent semantic validation or fresh embedding inference |
| Memory, skills, plugins, MCP | [Memory lifecycle](../labs/memory-lifecycle/README.md), [native skill invocation](../labs/skill-execution/README.md), and [MCP client/server](../examples/mcp-notes/README.md) | Local demonstrations delivered; broad host portability and production services not established |
| Integrated recovery and proposed updates | [Read-only capstone](../labs/capstone/README.md) and [resumed update](../labs/capstone-update/README.md) retain complete requests, outputs, checkpoints, and gate events | Initial integration delivered; controlled pause/failure and scripted reviewer remain distinct from real outage recovery or human approval |
| Failure handling and boundaries | [Repair](../labs/output-repair/README.md), [agent recovery](../labs/agent-recovery/README.md), [trust boundaries](../labs/trust-boundaries/README.md), and update gate | Actual model responses and authored host probes labeled separately; no adaptive attack-resistance or distributed exactly-once claim |
| Operational evaluation | [24-check report](../evaluation/report-2026-10-19-judge-tools.json), runtime manifests, [uncertainty example](../labs/eval-uncertainty/README.md), and [judge comparison](../evaluation/judge-calibration/README.md) | Integrity/checking tools delivered; actual human-reference judge calibration and invoice-backed cost comparisons absent |
| Independent evidence | [Blank annotation packet](../labs/natural-notes/review/blank.json), [blank reader form](FEEDBACK.md), and [simulated walkthrough](simulated-reader-2026-10-19.md) inspected | **Open:** blanks and AI feedback are not completed independent review |
| Maintenance process | [Recorded editorial pass](../updates/reviews/2026-10-19/README.md), nine-source collector, and [hosted artifact verification](../updates/reviews/2026-10-19/hosted-verification.json) | Initial process demonstrated; multiple runs on one day do not establish weekly continuity |
| Public presentation and privacy | README retains minimal entry navigation, MIT/contribution links, and star request; `git ls-files FLOW.md` returns no tracked file and `git check-ignore FLOW.md` confirms exclusion | Current-tree presentation/privacy invariant holds; no claim of rewriting historical commits |

The saved checkers were inspected for scope: representation checks verify recorded dimensions, attention constraints, cosine calculations, hashes, and the browser payload; the real-docs checker recomputes rankings from saved vectors, reconstructs requests, and regrades saved responses. Optional tokenizer replay is distinct from a normal offline check. None of those checks supplies new human labels or proves general model reliability.

## Outside evidence inspected

At this audit, the public GitHub issues API for this repository (`state=all`, first page of 100) returned an empty list, including no pull-request entries. The repository review directories contain the blank forms, checker/tests, and explicitly AI-simulated report; no completed independent submission is stored there. This does not establish that no one has privately reviewed the guide. The user has offered to ask readers, and any eventual private feedback needs consent before publication.

The source-watch run listing shows successful executions `39225299704` and `39256400637`, both dated 2026-10-19. The latter's retained artifact covers nine repositories. This proves hosted collection ran, not that a later weekly editorial cycle happened. The workflow has read-only repository permissions and does not automatically publish guidance or run model experiments.

## Concrete visual correction

The existing mobile overflow check passed even though table captions in the representation visual were partly outside the initially visible table area. Inspection of the generated screenshot exposed that distinction. Captions now sit outside horizontal scroll regions, with explicit scroll instructions and labeled keyboard-focusable regions for all three tables.

Targeted Chromium checks at 320 and 375 pixels confirm all captions fit within the viewport, keyboard Right Arrow scrolls the focused attention region, focus stays on that region, and the page itself has no horizontal overflow. The original browser control/data checks still pass. This is automated testing plus AI inspection of screenshots, not feedback from an actual person using assistive technology.

## Remaining work in order

1. Deliver the promised noncoding source-grounded research/revision case with all necessary source material, actual response, claim/citation checking, and clearly labeled failure material.
2. Incorporate actual beginner and developer reader feedback and independent annotations when received; preserve disagreements and consent. Do not substitute another persona simulation.
3. Run a frozen model-judge study against appropriate human-reviewed cases, keeping calibration and test groups separate. Existing exposed examples can support development, not a newly claimed blind test.
4. Complete and retain subsequent weekly editorial reviews as time and new evidence permit. More same-day collector executions cannot satisfy that requirement.

Broader architectures, multimodal accounting, production authorization, distributed actions, and broad adversarial studies remain explicitly identified extensions in the roadmap/core checklist. The listed open requirements above have not been silently reclassified as extensions or completed by this audit.

## Subsequent disposition: research/revision example

The [noncoding research/revision case](../everyday/research-revision/README.md) now supplies the previously missing implementation: two inspected primary sources, complete local notes, an authored failure draft, one actual revised response, a claim ledger, and separate mechanical/author checks. The audit above is preserved as the finding at its stated base commit. This resolves that content gap at demonstration level; it does not resolve independent reader feedback, annotations, actual judge calibration, or weekly continuity.
