"""Run a frozen five-condition example/decomposition comparison; max 12 calls."""

import argparse, hashlib, json, subprocess, tempfile, time
from pathlib import Path
from design import assemble, schedule, score

ROOT = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    out = a.output
    out.mkdir(parents=True, exist_ok=False)
    frozen = out / "frozen"
    frozen.mkdir()
    names = [
        "dataset.json",
        "rules.txt",
        "ledger.txt",
        "resolve.txt",
        "PROTOCOL.md",
        "design.py",
        "run.py",
    ]
    hashes = {}
    for name in names:
        raw = (ROOT / name).read_bytes()
        (frozen / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    dataset = json.loads((frozen / "dataset.json").read_text())
    cases = [c for c in dataset if c["split"] == "evaluation"]
    simple = [c for c in dataset if c["split"] == "simple"]
    boundary = [c for c in dataset if c["split"] == "boundary"]
    rules = (frozen / "rules.txt").read_text()
    manifest = {
        "sha256": hashes,
        "requested_model": "gpt-6.1-sol",
        "cli_version": subprocess.check_output(
            ["codex", "--version"], text=True
        ).strip(),
        "schedule": schedule(),
        "trials": [],
    }

    def save():
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    def call(name, prompt):
        (out / f"{name}.input.txt").write_text(prompt)
        output = out / f"{name}.output.txt"
        with tempfile.TemporaryDirectory(prefix="prompt-guide-examples-") as cwd:
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
                str(output.resolve()),
                "-",
            ]
            started = time.monotonic()
            try:
                result = subprocess.run(
                    cmd, input=prompt, text=True, capture_output=True, timeout=180
                )
                status = result.returncode
            except subprocess.TimeoutExpired:
                status = "timeout"
            row = {
                "name": name,
                "status": status,
                "seconds": round(time.monotonic() - started, 3),
                "input_characters": len(prompt),
                "command": cmd,
            }
        return row, output.read_text() if output.exists() else ""

    save()
    for entry in schedule():
        name = f"{entry['repeat']}-{entry['arm']}"
        trial = {**entry, "calls": []}
        manifest["trials"].append(trial)
        save()
        if entry["arm"] == "decomposed":
            prompt = assemble((frozen / "ledger.txt").read_text(), [], cases)
            row, ledger = call(name + "-ledger", prompt)
            trial["calls"].append(row)
            save()
            if row["status"] != 0:
                trial["score"] = score("", cases)
                trial["skipped_final"] = True
                save()
                continue
            prompt = (
                assemble(rules, boundary, [])
                + (frozen / "resolve.txt").read_text()
                + "\nLEDGER\n"
                + ledger
            )
        else:
            examples = {
                "none": [],
                "simple": simple,
                "boundary": boundary,
                "reversed": list(reversed(boundary)),
            }[entry["arm"]]
            prompt = assemble(rules, examples, cases)
        row, raw = call(name + "-final", prompt)
        trial["calls"].append(row)
        trial["score"] = score(raw if row["status"] == 0 else "", cases)
        save()
        print(name, trial["score"]["passed"], "/", len(cases), flush=True)


if __name__ == "__main__":
    main()
