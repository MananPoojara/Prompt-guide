"""Record one source-conditioned revision; no browsing by the experimental model."""

import argparse, hashlib, json, subprocess, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def request(root):
    return (
        (root / "prompt.txt").read_text()
        + "\nSOURCE NOTES\n"
        + (root / "sources.json").read_text()
        + "\nDRAFT\n"
        + (root / "draft.txt").read_text()
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for name in ["sources.json", "draft.txt", "prompt.txt", "PROTOCOL.md", "run.py"]:
        raw = (ROOT / name).read_bytes()
        hashes[name] = hashlib.sha256(raw).hexdigest()
    text = request(ROOT)
    (out / "input.txt").write_text(text)
    response = out / "output.txt"
    with tempfile.TemporaryDirectory(prefix="prompt-guide-research-") as cwd:
        command = [
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
            str(response),
            "-",
        ]
        version = subprocess.check_output(["codex", "--version"], text=True).strip()
        start = time.monotonic()
        try:
            result = subprocess.run(
                command, input=text, text=True, capture_output=True, timeout=180
            )
            status = result.returncode
        except subprocess.TimeoutExpired:
            status = "timeout"
        elapsed = round(time.monotonic() - start, 3)
    data = dict(
        source_sha256=hashes,
        input_sha256=hashlib.sha256(text.encode()).hexdigest(),
        output_sha256=hashlib.sha256(response.read_bytes()).hexdigest()
        if response.exists()
        else None,
        command=command,
        cli_version=version,
        requested_model="gpt-6.1-sol",
        status=status,
        elapsed_seconds=elapsed,
    )
    (out / "manifest.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
