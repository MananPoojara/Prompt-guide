"""Bounded JSON-action agent with durable call reservation and read-only tools."""

import argparse, hashlib, json, subprocess, tempfile, time
from pathlib import Path
from agent import initial
from recovery import dispatch

ROOT = Path(__file__).resolve().parent


def save(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--condition", choices=["transient", "denied"], default="transient"
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--stop-after", type=int)
    args = parser.parse_args()
    out = args.output.resolve()
    statepath = out / "state.json"
    if args.resume:
        state = json.loads(statepath.read_text())
        for name, digest in state["hashes"].items():
            if (
                hashlib.sha256((out / "frozen" / name).read_bytes()).hexdigest()
                != digest
            ):
                raise SystemExit("Frozen artifact changed")
        for name in ["agent.py", "run.py", "recovery.py"]:
            if (ROOT / name).read_bytes() != (out / "frozen" / name).read_bytes():
                raise SystemExit("Runner changed; resume with frozen runner")
        if state.get("pending"):
            raise SystemExit(
                "Interrupted call retained; inspect before recovery. No automatic retry."
            )
    else:
        out.mkdir(parents=True, exist_ok=False)
        (out / "frozen").mkdir()
        for name in ["agent.py", "recovery.py", "run.py", "prompt.txt", "PROTOCOL.md"]:
            (out / "frozen" / name).write_bytes((ROOT / name).read_bytes())
        corpus = json.loads(
            (ROOT.parent / "evidence-grounding/corpus.json").read_text()
        )[:2]
        save(out / "frozen/corpus.json", corpus)
        state = initial(6)
        state["condition"] = args.condition
        state["fault_used"] = False
        state["hashes"] = {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (out / "frozen").iterdir()
        }
        state["model"] = "gpt-6.1-sol"
        save(statepath, state)
    docs = json.loads((out / "frozen/corpus.json").read_text())
    started = state["calls"]
    while not state["done"] and state["calls"] < state["limit"]:
        state["calls"] += 1
        step = state["calls"]
        state["pending"] = True
        save(statepath, state)
        request = (
            (out / "frozen/prompt.txt").read_text()
            + "\nHistory:\n"
            + json.dumps(state["history"])
            + "\nCalls remaining including this one: "
            + str(state["limit"] - step + 1)
        )
        (out / f"{step}.input.txt").write_text(request)
        response = out / f"{step}.output.txt"
        with tempfile.TemporaryDirectory(prefix="prompt-guide-agent-") as cwd:
            cmd = [
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
                str(response),
                "-",
            ]
            start = time.monotonic()
            try:
                result = subprocess.run(
                    cmd, input=request, text=True, capture_output=True, timeout=180
                )
                status = result.returncode
                log = result.stdout + "\n" + result.stderr
            except subprocess.TimeoutExpired as exc:
                status = "timeout"
                log = str(exc)
        (out / f"{step}.log.txt").write_text(log)
        raw = response.read_text() if status == 0 and response.exists() else ""
        try:
            decision = json.loads(raw)
        except ValueError:
            decision = None
        tool = (
            dispatch(state, decision, docs, state["condition"])
            if status == 0
            else {"error": "Model call failed; stopping"}
        )
        state["history"].append(
            {
                "call": step,
                "decision": decision,
                "result": tool,
                "status": status,
                "elapsed_seconds": round(time.monotonic() - start, 3),
                "command": cmd,
            }
        )
        state["pending"] = False
        save(statepath, state)
        save(out / f"{step}.checkpoint.json", state)
        print(step, status, decision, tool, flush=True)
        if status != 0 or (args.stop_after and step - started >= args.stop_after):
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
