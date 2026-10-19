"""Record one planning response and a scripted clarification exchange."""

import argparse, hashlib, json, subprocess, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    out = a.output
    out.mkdir(parents=True, exist_ok=False)
    frozen = out / "frozen"
    frozen.mkdir()
    hashes = {}
    for name in [
        "planning.input.txt",
        "planning.prompt.txt",
        "clarification.input.txt",
        "clarification.prompt.txt",
        "user-reply.txt",
        "PROTOCOL.md",
        "run.py",
    ]:
        raw = (ROOT / name).read_bytes()
        (frozen / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    manifest = {
        "requested_model": "gpt-6.1-sol",
        "reasoning_effort": "low",
        "cli_version": subprocess.check_output(
            ["codex", "--version"], text=True
        ).strip(),
        "sha256": hashes,
        "calls": [],
    }

    def save():
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    def call(name, request):
        target = out / f"{name}.output.txt"
        (out / f"{name}.input.txt").write_text(request)
        with tempfile.TemporaryDirectory(prefix="prompt-guide-planning-") as cwd:
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
                str(target.resolve()),
                "-",
            ]
            started = time.monotonic()
            try:
                result = subprocess.run(
                    cmd, input=request, text=True, capture_output=True, timeout=180
                )
                status = result.returncode
            except subprocess.TimeoutExpired:
                status = "timeout"
        row = {
            "name": name,
            "status": status,
            "seconds": round(time.monotonic() - started, 3),
            "command": cmd,
            "input_sha256": hashlib.sha256(request.encode()).hexdigest(),
            "output_sha256": hashlib.sha256(target.read_bytes()).hexdigest()
            if target.exists()
            else None,
        }
        manifest["calls"].append(row)
        save()
        print(name, status, flush=True)
        return status, target.read_text() if target.exists() else ""

    save()
    planning = (
        (frozen / "planning.prompt.txt").read_text()
        + "\nSUPPLIED FACTS\n"
        + (frozen / "planning.input.txt").read_text()
    )
    call("planning", planning)
    question = (
        (frozen / "clarification.prompt.txt").read_text()
        + "\nREQUEST\n"
        + (frozen / "clarification.input.txt").read_text()
    )
    status, answer = call("question", question)
    if status == 0:
        followup = (
            "Continue this scripted conversation. Answer the latest user reply. Do not use tools.\n\nUSER\n"
            + question
            + "\nASSISTANT\n"
            + answer
            + "\nUSER\n"
            + (frozen / "user-reply.txt").read_text()
        )
        call("followup", followup)


if __name__ == "__main__":
    main()
