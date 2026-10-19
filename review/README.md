# Help verify that people can use the guide

[Start here](../START-HERE.md) · [Coverage audit](../CORE-COVERAGE.md) · [Contributing](../CONTRIBUTING.md)

**Status: no independent reader feedback or completed independent label review has been received.** This packet prepares the review; it is not evidence that the review happened. Participation is optional.

Choose the path that fits your experience. Read the linked pages, attempt the task, and record what you actually understood or could not do. Do not use another model to answer for you if the submission is intended as human evidence. If you used assistance, disclose it; assisted feedback can still identify useful problems.

## Beginner reader

Start with [the everyday planning example](../everyday/planning-clarification/planning.md) and [clarification example](../everyday/planning-clarification/clarification.md). No account, installation, or coding is required.

1. Explain why the optional spreadsheet does not fit without changing a supplied constraint.
2. Say which missing detail the model asked about before planning the workshop, and why that detail matters.
3. Change one constraint for a task of your own. Write the prompt you would use and name one thing you would check in its answer. You do not need to make a model call.
4. Identify any unfamiliar term, confusing transition, unreadable table, or place you needed another website to understand the example.

Report your own answer and the page or sentence that helped or confused you. Do not just report that the guide was “good.” We need evidence about where the explanation works or fails.

## Developer reader

Start with [real-document retrieval](../labs/real-docs/README.md) and [trust boundaries](../labs/trust-boundaries/README.md). Reading saved evidence needs no model account; running the following checks needs Python 3.10+. From the repository root (the folder containing `START-HERE.md`), run:

```bash
python3 labs/real-docs/view_results.py --method dense --question progress-type
python3 labs/trust-boundaries/check_saved.py
```

1. Explain how the progress-token answer can be correct while its complete-reference check fails. Identify the saved text that establishes this.
2. Identify the authored host probe that passes provenance but fails answer correctness. Distinguish that fixture from an observed model proposal.
3. Run the two commands if you can. Record your OS/Python version, the actual result, and any undocumented prerequisite. If you only read the artifacts, say so.
4. Identify a decision you could now make in your own system and a claim these small experiments do not justify.

## Accessibility and navigation

On either path, note whether the page remains usable with your preferred text size, narrow screen, keyboard navigation, or assistive technology. State what you actually tested; a visual glance is not a screen-reader test. No diagnosis, disability disclosure, or other sensitive information is needed.

## Independent label reviewer

The separate [twelve-note annotation packet](../labs/natural-notes/review/README.md) supports a different question: do the experiment's authored expected answers match an independent reading of its policy and notes? Complete it before looking at the answer key where possible, and disclose prior access. Since the key is public, enforced blinding is not claimed.

Do not treat a reader saying the guide is clear as approval of every label, or label agreement as proof that the guide teaches effectively. Model-judge calibration remains pending until appropriate human-reviewed cases and separate calibration/test sets exist.

## Record and share feedback

Use the [feedback form](FEEDBACK.md). Share only information you agree may appear publicly. A pull request or issue can contain the completed form; private feedback may also be summarized with permission. The maintainer must not publish private replies, personal details, or quotes without consent.

The maintainer should preserve original feedback, separate observed difficulties from proposed fixes, correct the relevant page, and ask for a targeted recheck when needed. Record reviewer attribution and assistance honestly. Review metadata is self-reported, not identity verification. Even successful feedback from a few people is limited qualitative evidence, not a representative usability study or universal certification.

## Simulated walkthrough

The [AI-simulated novice walkthrough](simulated-reader-2026-10-19.md) records local task answers and two documentation findings. The [fix record](fixes-2026-10-19.md) tracks their disposition. This is preparation for human review, not a completed human-review gate.
