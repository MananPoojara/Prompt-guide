"""Check token slicing, retained text, budget accounting, and archived source hashes."""

import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/run-2026-10-19"
data = json.loads((out / "data.json").read_text())
for name, digest in data["sha256"].items():
    assert hashlib.sha256((out / name).read_bytes()).hexdigest() == digest
rows = {r["condition"]: r for r in data["records"]}
budget = data["capacity"] - data["reserve"]
pieces = {}
for row in rows.values():
    assert len(row["ids"]) == len(row["pieces"]) == row["input_tokens"]
    assert (
        "".join(row["pieces"]) == row["text"]
    )  # This ASCII fixture has no split UTF-8 sequences.
    assert row["within_budget"] == (row["input_tokens"] <= budget)
    for token, piece in zip(row["ids"], row["pieces"]):
        if token in pieces:
            assert pieces[token] == piece
        pieces[token] = piece
full = rows["full"]
assert rows["prefix"]["ids"] == full["ids"][:budget]
assert rows["suffix"]["ids"] == full["ids"][-budget:]
assert not full["within_budget"]
assert (
    not rows["prefix"]["retained"]["question"]
    and not rows["suffix"]["retained"]["evidence"]
)
assert all(rows["packed"]["retained"].values()) and rows["packed"]["within_budget"]
assert rows["packed"]["text"] == data["packing"]["text"]
assert data["packing"]["input_tokens"] == rows["packed"]["input_tokens"]
assert data["packing"]["selected"] == ["approved"]
for name in ["instruction", "evidence", "question"]:
    # Recover exact segments from the recorded full packet's fixed ordering.
    original = full["text"].split("\n\n")[
        {"instruction": 0, "evidence": 1, "question": -1}[name]
    ]
    for row in rows.values():
        assert row["retained"][name] == (original in row["text"])
print(
    "Verified actual token slices, omitted/retained segments, budget, and frozen source hashes"
)
