"""Verify the recorded revision mechanically; author semantic review stays separate."""

import hashlib, json, re
from pathlib import Path
from run import request

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/run-2026-10-19"
manifest = json.loads((out / "manifest.json").read_text())
for name, digest in manifest["source_sha256"].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
text = request(ROOT)
assert text == (out / "input.txt").read_text()
assert hashlib.sha256(text.encode()).hexdigest() == manifest["input_sha256"]
raw = (out / "output.txt").read_bytes()
assert hashlib.sha256(raw).hexdigest() == manifest["output_sha256"]
assert manifest["status"] == 0
answer = json.loads(raw)
assert set(answer) == {"claims", "revised_explainer", "unresolved"}
expected = {
    "C1": ("contradicted", ["S1"]),
    "C2": ("contradicted", ["S1"]),
    "C3": ("contradicted", ["S2"]),
    "C4": ("supported_but_wrong_citation", ["S2"]),
    "C5": ("unsupported", []),
}
assert isinstance(answer["claims"], list) and len(answer["claims"]) == 5
assert {r["id"] for r in answer["claims"]} == set(expected)
for row in answer["claims"]:
    assert set(row) == {"id", "verdict", "supporting_sources"}
    assert (row["verdict"], row["supporting_sources"]) == expected[row["id"]]
paragraph = answer["revised_explainer"]
assert isinstance(paragraph, str) and 0 < len(paragraph.split()) <= 65
assert set(re.findall(r"\[(S\d+)\]", paragraph)) == {"S1", "S2"}
assert isinstance(answer["unresolved"], str) and answer["unresolved"].strip()
readme = (ROOT / "README.md").read_text()
assert "> " + paragraph in readme and "> " + answer["unresolved"] in readme
assert (ROOT / "prompt.txt").read_text() in readme
assert (ROOT / "draft.txt").read_text() in readme
review = json.loads((ROOT / "author-review.json").read_text())
assert review["independent_human_review"] is False
print(
    f"Verified source/input/output hashes, five authored claim labels, citation IDs, and {len(paragraph.split())}-word paragraph; semantic checks remain author-reviewed."
)
