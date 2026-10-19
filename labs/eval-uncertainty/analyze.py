"""Reproduce an exploratory paired cluster resampling example from saved retrieval data."""

import argparse, hashlib, json
from pathlib import Path
from uncertainty import cluster_bootstrap, wilson

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "retrieval/results/pilot-2026-10-19/data.json"


def analysis():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    conditions = {
        c["name"]: {r["query_id"]: r for r in c["results"]} for c in data["conditions"]
    }
    rows = []
    for q in data["queries"]:
        if q["split"] != "evaluation":
            continue
        baseline = int(conditions["bm25-128"][q["id"]]["evidence_coverage_at_3"])
        candidate = int(conditions["dense-128"][q["id"]]["evidence_coverage_at_3"])
        rows.append(
            {
                "query_id": q["id"],
                "cluster": q["document_id"],
                "baseline": baseline,
                "candidate": candidate,
                "delta": candidate - baseline,
            }
        )
    return {
        "analysis_type": "Exploratory conditional illustration; not population inference",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "metric": "complete reference-span coverage at top 3",
        "baseline": "bm25-128",
        "candidate": "dense-128",
        "paired_rows": rows,
        "wins": sum(r["delta"] > 0 for r in rows),
        "losses": sum(r["delta"] < 0 for r in rows),
        "ties": sum(r["delta"] == 0 for r in rows),
        "cluster_resampling": cluster_bootstrap(rows),
        "hypothetical_independent_trials": {
            "10_of_10_wilson_95": wilson(10, 10),
            "100_of_100_wilson_95": wilson(100, 100),
        },
        "identical_pairs_example": cluster_bootstrap(
            [{"cluster": str(i), "delta": 0} for i in range(10)], 1000, 42
        ),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=False)
    report = analysis()
    report["sha256"] = {}
    for name in ["analyze.py", "uncertainty.py", "PROTOCOL.md"]:
        raw = (ROOT / name).read_bytes()
        (a.output / name).write_bytes(raw)
        report["sha256"][name] = hashlib.sha256(raw).hexdigest()
    (a.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {
                k: v
                for k, v in report.items()
                if k in ["wins", "losses", "ties", "hypothetical_independent_trials"]
            },
            indent=2,
        )
    )
    print("Conditional resampling interval:", report["cluster_resampling"]["interval"])


if __name__ == "__main__":
    main()
