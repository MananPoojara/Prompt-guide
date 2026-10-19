# AI-simulated novice developer review — 2026-10-19

This is model-generated feedback from a simulated reader comfortable with basic Python and terminal commands but new to prompting, retrieval, agents, and MCP. It is **not independent human review**, an actual novice interview, or evidence of teaching effectiveness. The requested simulation used local files and offline inspection commands. No external website, fresh model call, package installation, publication, or commit was used. Published answers and reference labels were read; this review is not blinded.

## Tasks and actual results

Read `README.md`, `START-HERE.md`, and `review/README.md`, then followed the beginner planning/clarification pages and developer real-docs/trust-boundaries pages. Followed their local result links and inspected the glossary, earlier retrieval lab, context chapter excerpts, examples index, saved progress-token answer/source, and authored host probes. No applicable `AGENTS.md` was found in the repository or ancestor paths checked. `FLOW.md` and credential files were not read.

**Beginner task 1:** Required work takes 70 minutes; the fixed break and reserved buffer use another 20. The available 90 minutes are exhausted. The optional spreadsheet needs another 20 minutes, so it cannot fit while preserving all supplied constraints. `everyday/planning-clarification/planning.md:10-19` supplies the inputs and lines 41-55 explicitly check them. This answer required no outside explanation.

**Beginner task 2:** The model asks for the workshop's topic or goal (`everyday/planning-clarification/clarification.md:25`). That determines what the agenda should teach or produce. The scripted reply supplies the topic plus audience, duration, materials, and activity lengths; the page clearly labels it a fixture rather than a reader interview (lines 29-34).

**Beginner task 3 — constructed practice prompt, not executed:** “Prepare eight paper-craft kits from 10:00 to 11:50. Sort for 20 minutes, pack for 25 after sorting, label for 15 after packing, and clean for 10 after labeling. Keep the fixed 10:45–10:55 break and the final ten minutes unused. Only one person works and tasks cannot overlap or be shortened. The optional inventory spreadsheet takes 20 minutes. Return a start/end/activity table, explain whether the optional work fits, and check the total.” This changes the available-window constraint; the final-ten-minute buffer consequently moves to 11:40–11:50. Check that the spreadsheet fits at 11:20–11:40 without consuming the buffer, and the total is 110 minutes.

**Developer task 1:** The saved answer says `string or integer`, matching the expected value, and quotes an exact selected fragment. But its quote begins `s **MUST** be a string or integer value`, omitting the subject `Progress tokens`. The complete authored reference is therefore absent. The viewer reports `answer_correct: true`, `quote_in_selected_chunk: true`, `reference_in_quote: false`, and `supported: false`. Evidence: `labs/real-docs/results/pilot-2026-10-19/dense-progress-type.output.txt:1`; full source at `labs/real-docs/sources/basic-utilities-progress.mdx:18`; explanation at `labs/real-docs/RESULTS.md:33`. This is a failure of the documented strict reference rule, not proof the returned types are false.

**Developer task 2:** `wrong-answer-valid-provenance` in `labs/trust-boundaries/probes.json:8` proposes `09:00` while citing approved document `decision`. The host accepts the approved source but the answer-reference check fails because the approved time is `14:00`. `labs/trust-boundaries/RESULTS.md:27-33` explicitly distinguishes this authored probe from observed model output. All five observed proposals returned `14:00`; none demonstrates a live forbidden attempt being blocked.

**Developer task 3:** Environment reported `Linux 6.8.0-138-generic`, `Python 3.10.12`. From the repository root, both prescribed commands completed with exit code 0:

```text
python3 labs/real-docs/view_results.py --method dense --question progress-type
  Evidence tokens: 372 / 384; complete reference coverage: False
  Printed selected evidence, recorded answer, authored reference, and checks.

python3 labs/trust-boundaries/check_saved.py
  Verified five model proposals separately from nine authored host probes;
  provenance-only negative control retained
```

The viewer inspects saved data; the checker replays saved evidence. Neither result is a fresh model experiment. No extra package prerequisite surfaced. Also ran read-only file discovery, line-numbered reads, targeted text searches, `python3 --version`, and `uname -sr`. A deliberate working-directory reproduction is documented below. No full unit-test suite, retokenization, or fresh experiment was run.

**Developer task 4:** In a system I build, I would check source authorization and answer correctness separately, and inspect retrieved chunks before concluding that a failed support score means a factually wrong answer. These experiments do not establish a universally superior retrieval method or resistance to adaptive attacks.

## Prioritized findings

1. **P2 — state the command working directory. Observed omission and reproduced failure.** `review/README.md:22-27` gives Python requirements and root-relative commands without saying to run them from the repository root. Running its viewer command from `review/` exits 2 with `can't open file .../review/labs/real-docs/view_results.py`. Running from the root succeeds. Add “From the repository root (the folder containing START-HERE.md), run:” before the block. The lab command blocks at `labs/real-docs/README.md:43-59` and `labs/trust-boundaries/README.md:58-65` would benefit from the same note. This was a deliberate alternate-directory test, not a claim that a human reader actually got stuck there.

2. **P3 — map the retrieval method names at the direct developer entry point. Observed terminology gap; novice impact inferred.** `labs/real-docs/README.md:11-17` introduces BM25 and MiniLM, and lines 48-49 use `bm25` and `dense`, without a short explanation connecting those names. The glossary defines BM25 and embedding (`handbook/glossary.md:11,19`), but has no dense/MiniLM entry. The earlier retrieval lab offers the implementation table at `labs/retrieval/README.md:46-50`, yet that creates a detour from the review's suggested starting page. Add a sentence such as “BM25 ranks chunks by matching words; dense search compares numerical representations of meaning, here produced by MiniLM.” Link to the earlier lab for details. This gap did not prevent answering the concrete review questions, whose evidence is clearly presented.

## What worked and what remains untested

The beginner pages supplied complete facts, requests, outputs, and arithmetic; no confusing transition or necessary outside lookup was identified during this textual review. The developer viewer made the cropped quote and reference directly comparable. The distinction between recorded model proposals and authored probes, and the limits of the small experiments, was explicit and useful. The main index and Start Here links resolved to the local pages used in this review.

Inspection was through terminal text, not a rendered browser. No narrow-screen layout, enlarged text, keyboard interaction, screen reader, or visual table/diagram usability test was performed. No claim about accessibility follows from this review. The simulated persona cannot establish what an actual beginner would understand or how long their tasks would take. Independent human reader feedback remains outstanding.
