"""Inspect one saved evidence packet, answer, and independently defined reference."""

import argparse, json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--method", choices=["bm25", "dense"], required=True)
parser.add_argument("--question", required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent / "results/pilot-2026-10-19"
data = json.loads((root / "data.json").read_text())
row = next(
    (
        r
        for r in data["rows"]
        if r["method"] == args.method and r["query_id"] == args.question
    ),
    None,
)
if row is None:
    parser.error("Unknown question; inspect queries.json for available IDs")
q = next(q for q in data["queries"] if q["id"] == args.question)
print(q["question"])
print(
    f"Evidence tokens: {row['evidence_tokens']} / 384; complete reference coverage: {row['coverage']}"
)
print("\nSELECTED EVIDENCE\n" + row["packet"])
output = root / f"{args.method}-{args.question}.output.txt"
if output.exists():
    print("\nRECORDED ANSWER\n" + output.read_text())
print("\nAUTHORED REFERENCE (not appended to model input)\n" + q["evidence"])
if "grade" in row:
    print("\nCHECKS\n" + json.dumps(row["grade"], indent=2))
