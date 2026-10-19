"""Replay the recorded memory lifecycle against a fresh database, without model access."""

import hashlib
import json
import tempfile
from pathlib import Path
from run import scenario

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/run-2026-10-19"
saved = json.loads((out / "transcript.json").read_text())
for name, digest in saved["sha256"].items():
    assert hashlib.sha256((out / name).read_bytes()).hexdigest() == digest
with tempfile.TemporaryDirectory() as directory:
    events = scenario(Path(directory) / "fresh.sqlite")
assert events == saved["events"]
by_event = {event["event"]: event for event in events}
assert by_event["corrected-read"]["result"]["value"] == "Room B"
assert by_event["expired-read"]["result"] == {
    "status": "expired",
    "value": None,
    "revision": 2,
    "source": "decision-2",
}
assert by_event["retracted-read"]["result"]["value"] is None
assert len(by_event["history"]["records"]) == 3
assert by_event["assembled-context"]["packet"]["memory"][0]["value"] == "Room B"
print(
    "Fresh SQLite replay matches every event, correction, context packet, and stale-value boundary"
)
