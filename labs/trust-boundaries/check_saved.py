"""Replay dispatcher decisions and reconstruct inputs; no model or network calls."""

import hashlib, json
from pathlib import Path
from boundary import Host, parse
from run import prompt, correct

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/pilot-2026-10-19"
frozen = out / "frozen"
data = json.loads((out / "manifest.json").read_text())
for name, digest in data["sha256"].items():
    assert hashlib.sha256((frozen / name).read_bytes()).hexdigest() == digest, name
    assert (ROOT / name).read_bytes() == (frozen / name).read_bytes(), name
probes = json.loads((frozen / "probes.json").read_text())
assert len(data["authored_host_probes"]) == len(probes) == 9
for expected, record in zip(probes, data["authored_host_probes"]):
    assert all(record[k] == v for k, v in expected.items())
    result = Host().dispatch(expected["proposal"])
    assert result == record["result"]
    assert (
        result["status"] == expected["expected_status"]
        and correct(result) == record["reference_correct"]
    )
assert not next(
    p
    for p in data["authored_host_probes"]
    if p["id"] == "wrong-answer-valid-provenance"
)["reference_correct"]
conditions = json.loads((frozen / "conditions.json").read_text())
assert len(data["model_runs"]) == len(conditions) == 5
for c, row in zip(conditions, data["model_runs"]):
    assert row["condition"] == c["id"]
    assert (out / f"{c['id']}.input.txt").read_text() == prompt(c)
    proposal = None
    if row["status"] == 0:
        try:
            proposal = parse((out / f"{c['id']}.output.txt").read_text())
            result = Host().dispatch(proposal)
        except (ValueError, FileNotFoundError):
            result = {"status": "rejected", "reason": "Invalid JSON response"}
    else:
        result = {"status": "not_dispatched", "reason": "Model call failed"}
    assert (
        proposal == row["proposal"]
        and result == row["host_result"]
        and correct(result) == row["reference_correct"]
    )
print(
    "Verified five model proposals separately from nine authored host probes; provenance-only negative control retained"
)
