"""Inspect a recorded question and its retrieved evidence without installing a model."""

import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    data = json.loads((ROOT / "results/pilot-2026-10-19/data.json").read_text())
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--condition",
        choices=[c["name"] for c in data["conditions"]],
        default="dense-48",
    )
    p.add_argument(
        "--question", choices=[q["id"] for q in data["queries"]], default="double-write"
    )
    a = p.parse_args()
    q = next(q for q in data["queries"] if q["id"] == a.question)
    c = next(c for c in data["conditions"] if c["name"] == a.condition)
    r = next(r for r in c["results"] if r["query_id"] == a.question)
    chunks = {x["id"]: x for x in c["chunks"]}
    print("QUESTION:", q["question"])
    print("REFERENCE EVIDENCE:", q["evidence"])
    print("Complete reference span covered in top 3:", r["evidence_coverage_at_3"])
    for n, hit in enumerate(r["ranking"][:3], 1):
        chunk = chunks[hit["chunk_id"]]
        print(
            f"\n{n}. {chunk['id']} score={hit['score']:.6f} source characters [{chunk['start']}, {chunk['end']})\n{chunk['text']}"
        )


if __name__ == "__main__":
    main()
