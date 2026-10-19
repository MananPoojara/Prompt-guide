"""Replay the saved model actions and separate scripted approval probes offline."""

import argparse
import hashlib
import json
from pathlib import Path
from workflow import initial, reserve, dispatch
from run import parse, request
from review_fixture import review

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=ROOT / "results/resumed-2026-10-19")
    args = parser.parse_args()
    out = args.run
    saved = json.loads((out / "state.json").read_text())
    replay = initial()
    keys = list(replay)
    for name, digest in saved["hashes"].items():
        raw = (out / "frozen" / name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest
        assert raw == (ROOT / name).read_bytes(), (
            f"Current {name} differs; review replay compatibility explicitly"
        )
    assert (ROOT / "gate.py").read_bytes() == (
        ROOT.parent / "action-approval/gate.py"
    ).read_bytes()
    documents = json.loads((out / "frozen/documents.json").read_text())
    instruction = (out / "frozen/prompt.txt").read_text()
    assert 0 < len(saved["runs"]) <= 6
    for i, row in enumerate(saved["runs"], 1):
        assert row["step"] == i
        reserve(replay)
        text = request(replay, instruction)
        assert text == (out / f"{i}.input.txt").read_text()
        assert len(text.encode()) == row["input_bytes"] <= 16000
        output = out / f"{i}.output.txt"
        action = None
        if output.exists():
            assert (
                hashlib.sha256(output.read_bytes()).hexdigest() == row["output_sha256"]
            )
        else:
            assert row["output_sha256"] is None
        if row["status"] == 0 and output.exists():
            try:
                action = parse(output.read_text())
                result = dispatch(replay, action, documents)
            except (ValueError, TypeError):
                result = dict(error="invalid_json", retryable=False)
        else:
            replay["phase"] = "process_failed"
            result = dict(error="process_failed", retryable=False)
        replay["pending"] = False
        replay["history"].append(dict(action=action, result=result))
        checkpoint = json.loads((out / "checkpoints" / f"{i}.json").read_text())
        assert all(replay[k] == checkpoint[k] for k in keys)
    if replay["phase"] == "running" and replay["calls"] == 6:
        replay["phase"] = "budget_exhausted"
    assert all(replay[k] == saved[k] for k in keys)
    pause = json.loads((out / "pause-state.json").read_text())
    assert pause == json.loads(
        (out / "checkpoints" / f"{pause['calls']}.json").read_text()
    )
    assert pause["history"][-1]["result"] == dict(
        error="temporary_unavailable", retryable=True
    )
    assert not pause["pending"] and pause["fault_used"]
    assert saved["resumes"] == [
        dict(calls=pause["calls"], history_length=len(pause["history"]))
    ]
    source = (out / "review-fixture-source.py").read_bytes()
    assert source == (ROOT / "review_fixture.py").read_bytes()
    recorded = json.loads((out / "review-fixture.json").read_text())
    assert recorded["reviewer_sha256"] == hashlib.sha256(source).hexdigest()
    actual = review(replay)
    actual["reviewer_sha256"] = hashlib.sha256(source).hexdigest()
    assert recorded == actual
    print(
        f"Verified {saved['calls']} recorded model calls, pause/resume at call {pause['calls']}, phase={saved['phase']}, scripted review accepted={actual['accepted']}"
    )
    print("No model call or human approval is performed by this checker.")


if __name__ == "__main__":
    main()
