"""Record a bounded model-directed update proposal; pause after a controlled read failure."""

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path
from gate import Rejected
from workflow import initial, reserve, recover, dispatch, BEFORE

ROOT = Path(__file__).resolve().parent
FILES = [
    "workflow.py",
    "gate.py",
    "run.py",
    "prompt.txt",
    "documents.json",
    "PROTOCOL.md",
]


def save(path, data):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(path)


def parse(raw):
    if len(raw.encode()) > 8192:
        raise ValueError("Response too large")

    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                raise ValueError("Duplicate JSON key")
            result[k] = v
        return result

    return json.loads(raw, object_pairs_hook=unique)


def request(state, instruction):
    text = (
        instruction
        + "\nCURRENT PLAN\n"
        + BEFORE
        + "\nBEFORE SHA256\n"
        + state["before_sha256"]
        + "\nCOMPLETED HISTORY\n"
        + json.dumps(state["history"], ensure_ascii=False)
        + "\nCalls remaining including this one: "
        + str(state["limit"] - state["calls"] + 1)
        + "\n"
    )
    if len(text.encode()) > 16000:
        raise ValueError("Full request exceeds host byte ceiling")
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    out = args.output.resolve()
    statepath = out / "state.json"
    if args.resume:
        state = json.loads(statepath.read_text())
        recover(state)
        for name, digest in state["hashes"].items():
            raw = (out / "frozen" / name).read_bytes()
            if (
                hashlib.sha256(raw).hexdigest() != digest
                or raw != (ROOT / name).read_bytes()
            ):
                raise ValueError("Frozen source or runner changed; resume refused")
        state["resumes"].append(
            dict(calls=state["calls"], history_length=len(state["history"]))
        )
    else:
        out.mkdir(parents=True, exist_ok=False)
        (out / "frozen").mkdir()
        (out / "checkpoints").mkdir()
        hashes = {}
        for name in FILES:
            raw = (ROOT / name).read_bytes()
            (out / "frozen" / name).write_bytes(raw)
            hashes[name] = hashlib.sha256(raw).hexdigest()
        state = initial()
        state.update(
            hashes=hashes,
            model="gpt-6.1-sol",
            cli_version=subprocess.check_output(
                ["codex", "--version"], text=True
            ).strip(),
            runs=[],
            resumes=[],
        )
    save(statepath, state)
    documents = json.loads((out / "frozen/documents.json").read_text())
    instruction = (out / "frozen/prompt.txt").read_text()
    while state["phase"] == "running" and state["calls"] < state["limit"]:
        reserve(state)
        save(statepath, state)
        step = state["calls"]
        try:
            text = request(state, instruction)
        except ValueError:
            state["pending"] = False
            state["phase"] = "input_limit"
            save(statepath, state)
            return
        (out / f"{step}.input.txt").write_text(text)
        output = out / f"{step}.output.txt"
        with tempfile.TemporaryDirectory(prefix="prompt-guide-capstone-update-") as cwd:
            command = [
                "codex",
                "exec",
                "--ignore-user-config",
                "--ephemeral",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "-m",
                state["model"],
                "-c",
                'model_reasoning_effort="low"',
                "-C",
                cwd,
                "--output-last-message",
                str(output),
                "-",
            ]
            started = time.monotonic()
            try:
                process = subprocess.run(
                    command, input=text, text=True, capture_output=True, timeout=180
                )
                status = process.returncode
            except subprocess.TimeoutExpired:
                status = "timeout"
            elapsed = round(time.monotonic() - started, 3)
        action = None
        if status == 0 and output.exists():
            try:
                action = parse(output.read_text())
                result = dispatch(state, action, documents)
            except (ValueError, TypeError, Rejected):
                result = dict(error="invalid_json", retryable=False)
        else:
            state["phase"] = "process_failed"
            result = dict(error="process_failed", retryable=False)
        state["pending"] = False
        state["history"].append(dict(action=action, result=result))
        state["runs"].append(
            dict(
                step=step,
                command=command,
                status=status,
                elapsed_seconds=elapsed,
                input_bytes=len(text.encode()),
                output_sha256=hashlib.sha256(output.read_bytes()).hexdigest()
                if output.exists()
                else None,
            )
        )
        save(statepath, state)
        save(out / "checkpoints" / f"{step}.json", state)
        print(step, status, result, flush=True)
        if result.get("error") == "temporary_unavailable" and not args.resume:
            save(out / "pause-state.json", state)
            print(
                "Paused after completed transient read; resume in a new runner process.",
                flush=True,
            )
            return
    if state["phase"] == "running":
        state["phase"] = "budget_exhausted"
        save(statepath, state)


if __name__ == "__main__":
    main()
