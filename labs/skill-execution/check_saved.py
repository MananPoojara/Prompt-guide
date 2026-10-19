"""Check native discovery/invocation evidence and retained source integrity offline."""

import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/run-2026-10-19"
manifest = json.loads((out / "manifest.json").read_text())
for name, digest in manifest["sha256"].items():
    assert hashlib.sha256((out / "frozen" / name).read_bytes()).hexdigest() == digest
assert [r["condition"] for r in manifest["runs"]] == ["baseline", "skill"]
models = []
for run in manifest["runs"]:
    name = run["condition"]
    assert run["status"] == 0 and run["evidence_before"] == run["evidence_after"]
    events = json.loads((out / f"{name}.events.json").read_text())
    assert [e["type"] for e in events] == run["event_types"]
    init = next(e for e in events if e["type"] == "system" and e["subtype"] == "init")
    models.append(init["model"])
    assert set(init["tools"]) <= {"Read", "Glob", "Grep", "Skill"}
    calls = [
        b for e in events for b in e.get("content", []) if b.get("type") == "tool_use"
    ]
    results = [
        b
        for e in events
        for b in e.get("content", [])
        if b.get("type") == "tool_result"
    ]
    assert all(c["name"] in {"Read", "Glob", "Grep", "Skill"} for c in calls)
    assert any(
        c["name"] == "Read"
        and c["input"]["file_path"].endswith("/results/baseline.txt")
        for c in calls
    )
    assert any(
        c["name"] == "Read"
        and c["input"]["file_path"].endswith("/results/candidate.txt")
        for c in calls
    )
    final = next(e for e in reversed(events) if e["type"] == "result")
    assert final["subtype"] == "success" and not final["is_error"]
    assert (out / f"{name}.output.txt").read_text() == final["result"] + "\n"
    if name == "baseline":
        assert not init.get("skills") and not any(c["name"] == "Skill" for c in calls)
    else:
        assert "prompt-guide:inspect-evidence" in init["skills"]
        assert any(
            p["name"] == "prompt-guide" and p["version"] == "0.1.0"
            for p in init["plugins"]
        )
        invocation = next(
            c
            for c in calls
            if c["name"] == "Skill"
            and c["input"]["skill"] == "prompt-guide:inspect-evidence"
        )
        receipt = next(r for r in results if r["tool_use_id"] == invocation["id"])
        assert not receipt.get(
            "is_error", False
        ) and "Launching skill: prompt-guide:inspect-evidence" in str(
            receipt["content"]
        )
        for label in ["Claim", "Evidence", "Verdict", "Safer wording", "Missing check"]:
            assert "**" + label + ":" in final["result"]
assert models == ["claude-sonnet-5-5", "claude-sonnet-5-5"]
print(
    "Verified two native sessions, plugin discovery, successful Skill invocation, evidence reads, and unchanged files"
)
