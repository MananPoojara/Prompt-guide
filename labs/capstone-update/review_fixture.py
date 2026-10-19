"""Scripted review and disposable apply probes; never independent human approval."""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from gate import Gate, Rejected, digest
from workflow import BEFORE, EXPECTED


def review(state):
    proposal = state.get("proposal")
    evidence = state.get("resolved_evidence") or {}
    accepted = (
        state["phase"] == "awaiting_review"
        and proposal["content"] == EXPECTED
        and evidence.get("document_id") == "decision"
        and evidence.get("revision") == "v2"
        and "change the start time to 14:00" in evidence.get("quote", "")
    )
    record = dict(
        evidence_type="scripted reviewer and authored host probes; not human approval",
        accepted=accepted,
        events=[],
    )
    if not accepted:
        return record
    with tempfile.TemporaryDirectory(prefix="prompt-guide-reviewed-plan-") as tmp:
        root = Path(tmp)
        target = root / "plan.txt"
        target.write_text(BEFORE)
        gate = Gate(root)

        def rejected(label, p):
            before = target.read_bytes()
            try:
                gate.apply(p)
            except Rejected as exc:
                assert target.read_bytes() == before
                record["events"].append(
                    dict(step=label, result="rejected", reason=str(exc))
                )
            else:
                raise AssertionError("Forbidden apply succeeded")

        rejected("before_approval", proposal)
        identity = gate.approve(proposal)
        record["events"].append(dict(step="scripted_approval", digest=identity))
        rejected(
            "tampered_proposal",
            dict(proposal, content=proposal["content"] + "Unreviewed line\n"),
        )
        target.write_text("Concurrent edit fixture\n")
        rejected("stale_target", proposal)
        target.write_text(BEFORE)
        record["events"].append(
            dict(step="apply_original", result=gate.apply(proposal))
        )
        record["events"].append(
            dict(step="same_process_replay", result=gate.apply(proposal))
        )
        assert target.read_text() == EXPECTED
        record["final_content"] = target.read_text()
        record["proposal_digest"] = digest(proposal)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    out = args.run / "review-fixture.json"
    if out.exists():
        raise FileExistsError("Preserve existing review evidence")
    state = json.loads((args.run / "state.json").read_text())
    source = Path(__file__).read_bytes()
    (args.run / "review-fixture-source.py").write_bytes(source)
    result = review(state)
    result["reviewer_sha256"] = hashlib.sha256(source).hexdigest()
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
