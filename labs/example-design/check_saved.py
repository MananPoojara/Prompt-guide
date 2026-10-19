"""Reconstruct every input and regrade retained finals without calling a model."""

import hashlib, json
from pathlib import Path
from design import assemble, schedule, score

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/pilot-2026-10-19"
frozen = out / "frozen"
manifest = json.loads((out / "manifest.json").read_text())
for name, digest in manifest["sha256"].items():
    assert hashlib.sha256((frozen / name).read_bytes()).hexdigest() == digest, name
assert manifest["schedule"] == schedule()
assert [{k: t[k] for k in ["repeat", "arm"]} for t in manifest["trials"]] == schedule()
dataset = json.loads((frozen / "dataset.json").read_text())
cases = [c for c in dataset if c["split"] == "evaluation"]
simple = [c for c in dataset if c["split"] == "simple"]
boundary = [c for c in dataset if c["split"] == "boundary"]
rules = (frozen / "rules.txt").read_text()
assert len(cases) == 10 and len(simple) == len(boundary) == 2
assert len({c["id"] for c in dataset}) == 14
assert len(manifest["trials"]) == 10
for trial in manifest["trials"]:
    name = f"{trial['repeat']}-{trial['arm']}"
    for call in trial["calls"]:
        assert call["input_characters"] == len(
            (out / f"{call['name']}.input.txt").read_text()
        )
    if trial["arm"] == "decomposed":
        assert (out / f"{name}-ledger.input.txt").read_text() == assemble(
            (frozen / "ledger.txt").read_text(), [], cases
        )
        if trial["calls"][0]["status"] != 0:
            assert (
                trial["skipped_final"]
                and len(trial["calls"]) == 1
                and trial["score"] == score("", cases)
            )
            continue
        ledger = (out / f"{name}-ledger.output.txt").read_text()
        expected = (
            assemble(rules, boundary, [])
            + (frozen / "resolve.txt").read_text()
            + "\nLEDGER\n"
            + ledger
        )
        assert len(trial["calls"]) == 2
    else:
        examples = {
            "none": [],
            "simple": simple,
            "boundary": boundary,
            "reversed": list(reversed(boundary)),
        }[trial["arm"]]
        expected = assemble(rules, examples, cases)
        assert len(trial["calls"]) == 1
    assert (out / f"{name}-final.input.txt").read_text() == expected
    raw = (
        (out / f"{name}-final.output.txt").read_text()
        if trial["calls"][-1]["status"] == 0
        else ""
    )
    assert trial["score"] == score(raw, cases)
print(
    "Verified five fixed conditions, two repetitions, every assembled request and final score; intermediate ledger meaning is not automatically graded"
)
