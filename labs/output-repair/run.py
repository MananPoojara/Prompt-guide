"""Run one bounded model repair per authored fault fixture; consumes Codex usage."""

import argparse, hashlib, json, subprocess, tempfile, time
from pathlib import Path
from contract import validate, check_reference

ROOT = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    frozen = a.output / "frozen"
    frozen.mkdir()
    manifest = {
        "model": "gpt-6.1-sol",
        "reasoning_effort": "low",
        "sha256": {},
        "trials": [],
    }
    for name in ["fixtures.json", "prompt.txt", "contract.py", "run.py", "PROTOCOL.md"]:
        raw = (ROOT / name).read_bytes()
        (frozen / name).write_bytes(raw)
        manifest["sha256"][name] = hashlib.sha256(raw).hexdigest()

    def save():
        (a.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    save()
    for fixture in json.loads((frozen / "fixtures.json").read_text()):
        name = fixture["id"]
        errors = validate(fixture["candidate"], fixture["documents"])
        payload = {
            "documents": fixture["documents"],
            "candidate": fixture["candidate"],
            "validation_errors": errors,
        }
        request = (
            (frozen / "prompt.txt").read_text()
            + "\nINPUT:\n"
            + json.dumps(payload, indent=2)
            + "\n"
        )
        (a.output / f"{name}.input.txt").write_text(request)
        output = (a.output / f"{name}.output.txt").resolve()
        with tempfile.TemporaryDirectory(prefix="prompt-guide-repair-") as cwd:
            cmd = [
                "codex",
                "exec",
                "--ignore-user-config",
                "--ephemeral",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "-m",
                manifest["model"],
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
        (a.output / f"{name}.log.txt").write_text(log)
        raw = output.read_text() if status == 0 and output.exists() else ""
        trial = {
            "id": name,
            "status": status,
            "elapsed_seconds": round(time.monotonic() - start, 3),
            "command": cmd,
            "before": {
                "contract_errors": errors,
                "reference_match": check_reference(
                    fixture["candidate"], fixture["expected"]
                ),
            },
            "after": {
                "contract_errors": validate(raw, fixture["documents"]),
                "reference_match": check_reference(raw, fixture["expected"]),
            },
        }
        manifest["trials"].append(trial)
        save()
        print(name, trial["before"], trial["after"], flush=True)


if __name__ == "__main__":
    main()
