"""Regrade retained answers and recompute rankings; optional cached tokenizer replay."""

import argparse, hashlib, json, math
from pathlib import Path
from contract import pack, grade
from retrieval import bm25, rank, evidence_covered
from run import INSTRUCTION

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retokenize", action="store_true")
    args = parser.parse_args()
    out = ROOT / "results/pilot-2026-10-19"
    data = json.loads((out / "data.json").read_text())
    frozen = out / "frozen"
    for name, digest in data["metadata"]["sha256"].items():
        assert hashlib.sha256((frozen / name).read_bytes()).hexdigest() == digest, name
    manifest = json.loads((frozen / "sources/manifest.json").read_text())
    for item in manifest["files"]:
        assert (
            hashlib.sha256((frozen / "sources" / item["file"]).read_bytes()).hexdigest()
            == item["sha256"]
        )
        assert (ROOT / "sources" / item["file"]).read_bytes() == (
            frozen / "sources" / item["file"]
        ).read_bytes()
    queries = json.loads((frozen / "queries.json").read_text())
    assert queries == data["queries"]
    chunks = data["chunks"]
    assert len(data["vectors"]) == len(chunks)
    assert len(data["query_vectors"]) == len(queries)
    assert all(len(v) == 384 for v in data["vectors"] + data["query_vectors"])
    byid = {c["id"]: c for c in chunks}
    assert len(byid) == len(chunks)
    for c in chunks:
        source = (frozen / "sources" / f"{c['document_id']}.mdx").read_text()
        assert source[c["start"] : c["end"]] == c["text"]
    for q in queries:
        source = (frozen / "sources" / f"{q['document_id']}.mdx").read_text()
        assert source[q["start"] : q["end"]] == q["evidence"]
    count = None
    if args.retokenize:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(
            data["metadata"]["encoder"],
            revision=data["metadata"]["revision"],
            local_files_only=True,
        )
        count = lambda s: len(tokenizer.encode(s, add_special_tokens=False))
    assert len(data["rows"]) == 16
    assert [(r["method"], r["query_id"]) for r in data["rows"]] == [
        (m, q["id"]) for m in ["bm25", "dense"] for q in queries
    ]
    for row in data["rows"]:
        qi = next(i for i, q in enumerate(queries) if q["id"] == row["query_id"])
        q = queries[qi]
        assert len(row["scores"]) == len(chunks)
        scores = (
            bm25(q["question"], chunks)
            if row["method"] == "bm25"
            else [
                sum(x * y for x, y in zip(data["query_vectors"][qi], v))
                for v in data["vectors"]
            ]
        )
        assert all(
            math.isclose(x, y, rel_tol=0, abs_tol=1e-10)
            for x, y in zip(scores, row["scores"])
        )
        order = rank(chunks, scores)
        assert row["ranking"] == [chunks[i]["id"] for i in order]
        selected = [byid[id] for id in row["selected"]]
        assert len(set(row["selected"])) == len(selected)
        assert row["selected"] == [id for id in row["ranking"] if id in row["selected"]]
        assert row["packet"] == "\n\n".join(
            f"[{c['id']}]\n{c['text']}" for c in selected
        )
        assert row["evidence_tokens"] == len(row["packet_token_ids"]) <= 384
        assert row["coverage"] == evidence_covered(q, selected)
        if count:
            chosen, packet, tokens = pack(chunks, order, count, 384)
            assert (
                [c["id"] for c in chosen] == row["selected"]
                and packet == row["packet"]
                and tokens == row["evidence_tokens"]
            )
            assert (
                tokenizer.encode(packet, add_special_tokens=False)
                == row["packet_token_ids"]
            )
        if row["split"] != "evaluation":
            continue
        name = f"{row['method']}-{q['id']}"
        prompt = (
            INSTRUCTION
            + "\nQUESTION\n"
            + q["question"]
            + "\n\nEVIDENCE\n"
            + row["packet"]
            + "\n"
        )
        assert (out / f"{name}.input.txt").read_text() == prompt
        assert row["call"]["input_characters"] == len(prompt)
        output = out / f"{name}.output.txt"
        try:
            parsed = json.loads(output.read_text()) if output.exists() else None
        except json.JSONDecodeError:
            parsed = None
        assert grade(parsed, q, selected) == row["grade"]
        assert row["abstained"] == (
            isinstance(parsed, dict) and parsed.get("status") == "insufficient_evidence"
        )
    print(
        "Verified six source snapshots, 16 retrieval rows, and 12 recorded answer attempts"
        + (
            " with exact tokenizer/packing replay"
            if count
            else " (token counts recorded, not retokenized)"
        )
    )


if __name__ == "__main__":
    main()
