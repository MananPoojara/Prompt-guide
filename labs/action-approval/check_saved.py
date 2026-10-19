"""Verify the recorded proposal and repeat the host gate in a new temporary directory."""

import hashlib, json
from pathlib import Path
from gate import parse_proposal, sha
from run import demonstrate, BEFORE

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/run-2026-10-19"
result = json.loads((out / "result.json").read_text())
for name, digest in result["sha256"].items():
    assert hashlib.sha256((out / "frozen" / name).read_bytes()).hexdigest() == digest
assert result["status"] == 0
payload = {
    "target": "plan.txt",
    "before_sha256": sha(BEFORE.encode()),
    "current_content": BEFORE,
    "decision": "The approved start time is now 14:00. Capacity remains 20.",
}
assert (out / "input.txt").read_text() == (
    out / "frozen/prompt.txt"
).read_text() + "\nINPUT:\n" + json.dumps(payload, indent=2) + "\n"
proposal = parse_proposal((out / "output.txt").read_text())
assert proposal == result["proposal"]
assert demonstrate(proposal) == result["demonstration"]
assert [e["event"] for e in result["demonstration"]["events"]] == [
    "unapproved-rejected",
    "scripted-review-approved",
    "tampered-rejected",
    "apply",
    "replay",
]
print(
    "Verified actual proposal, exact request, approval binding, tamper rejection, and local apply/replay"
)
