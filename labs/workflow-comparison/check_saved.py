"""Reconstruct every request/tool action and regrade the twelve recorded task runs."""

import hashlib, importlib.util, json
from pathlib import Path
from agent import initial, act
from workflow import QUESTIONS, initial_payload, summarize

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/pilot-2026-10-19"
frozen = out / "frozen"
report = json.loads((out / "manifest.json").read_text())
for name, digest in report["sha256"].items():
    assert hashlib.sha256((frozen / name).read_bytes()).hexdigest() == digest
spec = importlib.util.spec_from_file_location(
    "frozen_grounding", frozen / "grounding.py"
)
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)
corpus = json.loads((frozen / "corpus.json").read_text())
expected_order = [
    f"{repeat}-{task}-{strategy}"
    for repeat in [1, 2]
    for task in ["routine", "conflict"]
    for strategy in (
        ["single", "fixed", "agent"] if repeat == 1 else ["agent", "fixed", "single"]
    )
]
assert [run["id"] for run in report["runs"]] == expected_order
for run in report["runs"]:
    directory = out / run["id"]
    assert json.loads((directory / "result.json").read_text()) == run
    documents = corpus[:2] if run["task"] == "routine" else corpus[:3]
    state = initial(6)
    trace = []
    answers = []
    assert 1 <= len(run["calls"]) <= (6 if run["strategy"] == "agent" else 1)
    for number, call in enumerate(run["calls"], 1):
        if run["strategy"] == "agent":
            payload = {
                "questions": QUESTIONS,
                "history": trace,
                "remaining_calls_including_this": 7 - number,
            }
            prompt = "agent-prompt.txt"
        else:
            payload = initial_payload(run["strategy"], documents)
            prompt = "answer-prompt.txt"
            assert (
                json.loads((directory / "selected-documents.json").read_text())
                == payload["documents"]
            )
        request = (
            (frozen / prompt).read_text()
            + "\nINPUT:\n"
            + json.dumps(payload, indent=2)
            + "\n"
        )
        assert (directory / f"{number}.input.txt").read_text() == request and call[
            "request_characters"
        ] == len(request)
        if call["status"] == 0:
            raw = (directory / f"{number}.output.txt").read_text()
            try:
                parsed = json.loads(raw)
            except ValueError:
                parsed = None
            assert parsed == call["parsed"]
        else:
            parsed = None
        if run["strategy"] == "agent" and call["status"] == 0:
            result = act(state, parsed, documents)
            trace.append({"decision": parsed, "result": result})
            if result.get("accepted"):
                answers = result["answers"]
        elif run["strategy"] != "agent":
            answers = parsed if isinstance(parsed, list) else []
    assert (
        trace == run["trace"]
        and answers == run["answers"]
        and summarize(run["calls"]) == run["metrics"]
    )
    assert (
        grader.grade(
            json.dumps(answers),
            grader.expected(
                "current_top1" if run["task"] == "routine" else "conflicting_current"
            ),
            documents,
        )
        == run["score"]
    )
print(
    "Verified twelve task runs, exact requests, selection/tool traces, accounting, and reference scores"
)
