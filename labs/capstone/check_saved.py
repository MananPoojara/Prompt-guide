"""Replay the retained capstone trace without model calls; optional cached tokenization."""

import argparse
import hashlib
import json
from pathlib import Path
from pipeline import retrieve, render, assemble, parse, grade

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=ROOT / "results/pilot-2026-10-19")
    parser.add_argument("--retokenize", action="store_true")
    args = parser.parse_args()
    run = args.run
    data = json.loads((run / "manifest.json").read_text())
    for name, digest in data["sha256"].items():
        assert (
            hashlib.sha256((run / "frozen" / name).read_bytes()).hexdigest() == digest
        )
        assert (ROOT / name).read_bytes() == (run / "frozen" / name).read_bytes(), (
            f"Current {name} differs; review replay compatibility explicitly"
        )
    docs = json.loads((run / "frozen/documents.json").read_text())
    questions = json.loads((run / "frozen/questions.json").read_text())
    assert len(data["rows"]) == 20
    assert len({r["id"] for r in data["rows"]}) == 20
    assert {(r["method"], r["question_id"]) for r in data["rows"]} == {
        (m, q["id"]) for m in ("top1", "top3") for q in questions
    }
    tokenizer = None
    if args.retokenize:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(
            data["tokenizer"],
            revision=data["tokenizer_revision"],
            local_files_only=True,
        )
    totals = {"top1": 0, "top3": 0}
    calls = 0
    for row in data["rows"]:
        q = next(q for q in questions if q["id"] == row["question_id"])
        assert row["split"] == q["split"]
        ranked = retrieve(docs, q)
        assert ranked == row["ranked"]
        selected = row["selected"]
        limit = 1 if row["method"] == "top1" else 3
        assert len(selected) <= limit
        assert len({c["id"] for c in selected}) == len(selected)
        assert all(c in ranked for c in selected)
        assert [ranked.index(c) for c in selected] == sorted(
            ranked.index(c) for c in selected
        )
        request = render(q, selected)
        assert request == (run / f"{row['id']}.input.txt").read_text()
        assert len(request) == row["input_characters"]
        assert len(row["input_token_ids"]) <= data["input_budget"] == 1024
        if tokenizer:
            encode = lambda text: tokenizer.encode(
                text, add_special_tokens=False, truncation=False
            )
            assert encode(request) == row["input_token_ids"]
            assert assemble(q, ranked, limit, lambda text: len(encode(text)), 1024) == (
                request,
                selected,
            )
        if q["split"] == "development":
            assert row["status"] == "not_called"
            continue
        calls += 1
        output = run / f"{row['id']}.output.txt"
        answer = None
        if output.exists():
            assert (
                hashlib.sha256(output.read_bytes()).hexdigest() == row["output_sha256"]
            )
            if row["status"] == 0:
                try:
                    answer = parse(output.read_text())
                except (ValueError, TypeError):
                    pass
        else:
            assert row["output_sha256"] is None
        result = grade(answer, q, selected)
        assert result == row["grade"]
        totals[row["method"]] += result["passed"]
    assert calls == 16
    print(
        f"Verified 16 recorded calls and 4 development retrieval traces; strict authored-reference passes: {totals}"
    )
    print(
        "Tokenizer/greedy packing replay: "
        + (
            "performed"
            if tokenizer
            else "not performed; use --retokenize with cached pinned tokenizer"
        )
    )


if __name__ == "__main__":
    main()
