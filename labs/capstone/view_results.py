"""Read the actual evidence and output for one saved question, without inference."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--question", default="conflict")
args = parser.parse_args()
run = ROOT / "results/pilot-2026-10-19"
data = json.loads((run / "manifest.json").read_text())
rows = [r for r in data["rows"] if r["question_id"] == args.question]
if not rows:
    parser.error("Unknown question ID; inspect questions.json")
questions = json.loads((run / "frozen/questions.json").read_text())
question = next(q for q in questions if q["id"] == args.question)
print("QUESTION:", question["question"])
print("AUTHORED REFERENCE (not independent review):", json.dumps(question, indent=2))
for row in rows:
    print("\nMETHOD:", row["method"])
    print("Proxy input tokens:", len(row["input_token_ids"]))
    print("SELECTED EVIDENCE:", json.dumps(row["selected"], indent=2))
    output = run / f"{row['id']}.output.txt"
    print(
        "RECORDED OUTPUT:",
        output.read_text() if output.exists() else "(no final output)",
    )
    print("PROCESS STATUS:", row["status"])
    print("CHECKS:", json.dumps(row.get("grade"), indent=2))
