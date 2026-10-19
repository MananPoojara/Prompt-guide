# Independent annotation packet

**Status: no independent human labels have been received.** The published blank packet is not a completed review.

The [packet](blank.json) includes the twelve held-out notes without the gold answers or author rationales. Since the answer key is public elsewhere, this cannot enforce blindness. A reviewer should label the packet before inspecting the key and disclose any prior access.

For each case, fill in the owner and deadline, mark the judgment `confirmed` or `uncertain`, and add a comment explaining any ambiguity. `null` is a legitimate label for an unconfirmed field; leaving a row marked `unreviewed` means no annotation has been supplied. The tool never counts those blank rows as agreements.

Supply a reviewer name or credited identifier, date, type, and an honest declaration of independence. A model-generated annotation must use type `model`. Reviewer metadata is self-reported, not identity verification.

Compare a submitted packet with the gold labels:

```bash
python3 labs/natural-notes/review/review.py /path/to/submitted-packet.json
```

The report lists agreements, disagreements, uncertainty, and missing review. Even a complete matching human packet is only eligible for maintainer review; the script does not certify independent review or automatically approve the dataset. If a correction is needed, preserve the disagreement, version the labels, and rerun the affected experiment separately. Never silently alter the earlier gold answers or outputs.

You can test the review tool without a model account:

```bash
python3 -m unittest discover -s labs/natural-notes/review -p 'test_*.py'
python3 labs/natural-notes/review/review.py labs/natural-notes/review/blank.json
```

Contributing annotations is optional. Do not include personal or confidential information in a public submission.
