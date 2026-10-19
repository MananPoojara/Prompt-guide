"""Run a predeclared three-strategy comparison; consumes at most 32 Codex calls."""

import argparse, hashlib, json, subprocess, tempfile, time
from pathlib import Path
from agent import initial, act
from workflow import QUESTIONS, initial_payload, summarize

ROOT = Path(__file__).resolve().parent


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def call(directory, number, request):
    (directory / f"{number}.input.txt").write_text(request)
    output = (directory / f"{number}.output.txt").resolve()
    with tempfile.TemporaryDirectory(prefix="prompt-guide-workflow-") as cwd:
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
    (directory / f"{number}.log.txt").write_text(log)
    raw = output.read_text() if status == 0 and output.exists() else ""
    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = None
    return {
        "status": status,
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "request_characters": len(request),
        "command": cmd,
        "parsed": parsed,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    frozen = a.output / "frozen"
    frozen.mkdir()
    hashes = {}
    for name in [
        "run.py",
        "workflow.py",
        "agent.py",
        "answer-prompt.txt",
        "agent-prompt.txt",
        "PROTOCOL.md",
    ]:
        raw = (ROOT / name).read_bytes()
        (frozen / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    for name in ["corpus.json", "grounding.py"]:
        raw = (ROOT.parent / "evidence-grounding" / name).read_bytes()
        (frozen / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "frozen_grounding", frozen / "grounding.py"
    )
    grader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(grader)
    corpus = json.loads((frozen / "corpus.json").read_text())
    report = {
        "model": "gpt-6.1-sol",
        "reasoning_effort": "low",
        "sha256": hashes,
        "runs": [],
    }
    save(a.output / "manifest.json", report)
    for repeat in [1, 2]:
        for task in ["routine", "conflict"]:
            documents = corpus[:2] if task == "routine" else corpus[:3]
            for strategy in (
                ["single", "fixed", "agent"]
                if repeat == 1
                else ["agent", "fixed", "single"]
            ):
                name = f"{repeat}-{task}-{strategy}"
                directory = a.output / name
                directory.mkdir()
                calls = []
                trace = []
                answers = []
                if strategy != "agent":
                    payload = initial_payload(strategy, documents)
                    save(directory / "selected-documents.json", payload["documents"])
                    request = (
                        (frozen / "answer-prompt.txt").read_text()
                        + "\nINPUT:\n"
                        + json.dumps(payload, indent=2)
                        + "\n"
                    )
                    result = call(directory, 1, request)
                    calls.append(result)
                    answers = (
                        result["parsed"] if isinstance(result["parsed"], list) else []
                    )
                else:
                    state = initial(6)
                    while not state["done"] and state["calls"] < state["limit"]:
                        state["calls"] += 1
                        save(directory / "state.json", state)
                        payload = {
                            "questions": QUESTIONS,
                            "history": trace,
                            "remaining_calls_including_this": state["limit"]
                            - state["calls"]
                            + 1,
                        }
                        request = (
                            (frozen / "agent-prompt.txt").read_text()
                            + "\nINPUT:\n"
                            + json.dumps(payload, indent=2)
                            + "\n"
                        )
                        result = call(directory, state["calls"], request)
                        calls.append(result)
                        if result["status"] != 0:
                            break
                        tool_result = act(state, result["parsed"], documents)
                        trace.append(
                            {"decision": result["parsed"], "result": tool_result}
                        )
                        state["history"] = trace
                        save(directory / "state.json", state)
                        if tool_result.get("accepted"):
                            answers = tool_result["answers"]
                score = grader.grade(
                    json.dumps(answers),
                    grader.expected(
                        "current_top1" if task == "routine" else "conflicting_current"
                    ),
                    documents,
                )
                record = {
                    "id": name,
                    "repeat": repeat,
                    "task": task,
                    "strategy": strategy,
                    "calls": calls,
                    "trace": trace,
                    "answers": answers,
                    "score": score,
                    "metrics": summarize(calls),
                }
                save(directory / "result.json", record)
                report["runs"].append(record)
                save(a.output / "manifest.json", report)
                print(
                    name,
                    record["metrics"]["calls"],
                    "calls",
                    score["passed"],
                    "correct",
                    score["resolved"],
                    "resolved",
                    flush=True,
                )


if __name__ == "__main__":
    main()
