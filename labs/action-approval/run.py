"""Record one model proposal and a scripted approval-gate demonstration in a temporary directory."""

import argparse, hashlib, json, subprocess, tempfile, time
from pathlib import Path
from gate import Gate, Rejected, sha, digest, parse_proposal

ROOT = Path(__file__).resolve().parent
BEFORE = "Start: 13:00\nCapacity: 20\n"
AFTER = "Start: 14:00\nCapacity: 20\n"


def demonstrate(proposal):
    expected = {
        "target": "plan.txt",
        "before_sha256": sha(BEFORE.encode()),
        "content": AFTER,
    }
    events = []
    with tempfile.TemporaryDirectory(prefix="prompt-guide-approval-") as directory:
        root = Path(directory)
        (root / "plan.txt").write_text(BEFORE)
        gate = Gate(root)
        try:
            gate.apply(proposal)
        except Rejected as exc:
            events.append({"event": "unapproved-rejected", "reason": str(exc)})
        else:
            raise AssertionError("Unapproved proposal applied")
        if proposal != expected:
            events.append(
                {
                    "event": "scripted-review-rejected",
                    "reason": "Proposal differs from the expected fixture edit",
                }
            )
            return {"events": events, "final": (root / "plan.txt").read_text()}
        identity = gate.approve(proposal)
        events.append(
            {
                "event": "scripted-review-approved",
                "proposal_digest": identity,
                "reviewer": "scripted fixture, not a human",
            }
        )
        try:
            gate.apply({**proposal, "content": AFTER + "unreviewed addition\n"})
        except Rejected as exc:
            events.append({"event": "tampered-rejected", "reason": str(exc)})
        else:
            raise AssertionError("Tampered proposal applied")
        events.append({"event": "apply", "result": gate.apply(proposal)})
        events.append({"event": "replay", "result": gate.apply(proposal)})
        return {"events": events, "final": (root / "plan.txt").read_text()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    frozen = a.output / "frozen"
    frozen.mkdir()
    hashes = {}
    for name in ["gate.py", "run.py", "prompt.txt", "PROTOCOL.md"]:
        raw = (ROOT / name).read_bytes()
        (frozen / name).write_bytes(raw)
        hashes[name] = sha(raw)
    payload = {
        "target": "plan.txt",
        "before_sha256": sha(BEFORE.encode()),
        "current_content": BEFORE,
        "decision": "The approved start time is now 14:00. Capacity remains 20.",
    }
    request = (
        (frozen / "prompt.txt").read_text()
        + "\nINPUT:\n"
        + json.dumps(payload, indent=2)
        + "\n"
    )
    (a.output / "input.txt").write_text(request)
    output = (a.output / "output.txt").resolve()
    with tempfile.TemporaryDirectory(prefix="prompt-guide-proposal-model-") as cwd:
        cmd = [
            "codex",
            "exec",
            "--ignore-user-config",
            "--ephemeral",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "-m",
            "gpt-6.1-sol",
            "-c",
            'model_reasoning_effort="low"',
            "-C",
            cwd,
            "--output-last-message",
            str(output),
            "-",
        ]
        start = time.monotonic()
        try:
            r = subprocess.run(
                cmd, input=request, text=True, capture_output=True, timeout=180
            )
            status = r.returncode
            log = r.stdout + "\n" + r.stderr
        except subprocess.TimeoutExpired as exc:
            status = "timeout"
            log = str(exc)
    (a.output / "execution.log").write_text(log)
    report = {
        "model": "gpt-6.1-sol",
        "reasoning_effort": "low",
        "sha256": hashes,
        "command": cmd,
        "status": status,
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }
    try:
        if status != 0:
            raise ValueError("Model call failed")
        proposal = parse_proposal(output.read_text())
        digest(proposal)
        report["proposal"] = proposal
        report["demonstration"] = demonstrate(proposal)
    except (ValueError, Rejected) as exc:
        report["error"] = str(exc)
    (a.output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report.get("demonstration", report.get("error")), indent=2))


if __name__ == "__main__":
    main()
