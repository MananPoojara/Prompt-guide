"""Record 16 bounded model calls for the frozen read-only capstone."""

import argparse
import hashlib
import json
import platform
import subprocess
import tempfile
import time
from pathlib import Path
from pipeline import retrieve, assemble, parse, grade

ROOT = Path(__file__).resolve().parent
TOKENIZER = "sentence-transformers/all-MiniLM-L6-v2"
REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Disable tokenizer downloads; model calls still use the hosted service",
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    frozen = args.output / "frozen"
    frozen.mkdir()
    hashes = {}
    for name in [
        "pipeline.py",
        "run.py",
        "documents.json",
        "questions.json",
        "PROTOCOL.md",
    ]:
        raw = (ROOT / name).read_bytes()
        (frozen / name).write_bytes(raw)
        hashes[name] = hashlib.sha256(raw).hexdigest()
    from transformers import AutoTokenizer
    from importlib.metadata import version

    tokenizer = AutoTokenizer.from_pretrained(
        TOKENIZER, revision=REVISION, local_files_only=args.offline
    )

    def tokens(text):
        return tokenizer.encode(text, add_special_tokens=False, truncation=False)

    documents = json.loads((frozen / "documents.json").read_text())
    questions = json.loads((frozen / "questions.json").read_text())
    data = dict(
        sha256=hashes,
        tokenizer=TOKENIZER,
        tokenizer_revision=REVISION,
        input_budget=1024,
        reserved_output_proxy_units=256,
        requested_model="gpt-6.1-sol",
        python=platform.python_version(),
        transformers=version("transformers"),
        tokenizers=version("tokenizers"),
        cli_version=subprocess.check_output(["codex", "--version"], text=True).strip(),
        rows=[],
    )
    path = args.output / "manifest.json"

    def save():
        path.write_text(json.dumps(data, indent=2) + "\n")

    for method, limit in [("top1", 1), ("top3", 3)]:
        for q in questions:
            ranked = retrieve(documents, q)
            request, selected = assemble(
                q, ranked, limit, lambda t: len(tokens(t)), 1024
            )
            row = dict(
                id=f"{method}-{q['id']}",
                method=method,
                question_id=q["id"],
                split=q["split"],
                ranked=ranked,
                selected=selected,
                input_token_ids=tokens(request),
                input_characters=len(request),
                status="not_called",
            )
            (args.output / f"{row['id']}.input.txt").write_text(request)
            data["rows"].append(row)
    save()
    calls = 0
    for row in data["rows"]:
        if row["split"] != "evaluation":
            continue
        assert calls < 16
        calls += 1
        q = next(q for q in questions if q["id"] == row["question_id"])
        request = (args.output / f"{row['id']}.input.txt").read_text()
        output = args.output / f"{row['id']}.output.txt"
        with tempfile.TemporaryDirectory(prefix="prompt-guide-capstone-") as cwd:
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
                str(output.resolve()),
                "-",
            ]
            started = time.monotonic()
            try:
                process = subprocess.run(
                    command, input=request, text=True, capture_output=True, timeout=180
                )
                status = process.returncode
            except subprocess.TimeoutExpired:
                status = "timeout"
            row.update(
                command=command,
                status=status,
                elapsed_seconds=round(time.monotonic() - started, 3),
            )
        answer = None
        if status == 0 and output.exists():
            try:
                answer = parse(output.read_text())
            except (ValueError, TypeError):
                pass
        row["grade"] = grade(answer, q, row["selected"])
        row["output_sha256"] = (
            hashlib.sha256(output.read_bytes()).hexdigest() if output.exists() else None
        )
        save()
        print(row["id"], status, row["grade"], flush=True)


if __name__ == "__main__":
    main()
