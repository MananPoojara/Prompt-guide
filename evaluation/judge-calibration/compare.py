"""Compare declared reference labels and judge verdicts; no inference or certification."""

import argparse
import json
from pathlib import Path


def ratio(numerator, denominator):
    return dict(
        numerator=numerator,
        denominator=denominator,
        value=numerator / denominator if denominator else None,
    )


def compare(data):
    if not isinstance(data, dict) or set(data) != {
        "evidence_type",
        "reference_provenance",
        "judge_provenance",
        "rows",
    }:
        raise ValueError(
            "Expected evidence_type, reference_provenance, judge_provenance, rows"
        )
    if data["evidence_type"] not in ("synthetic_fixture", "submitted_comparison"):
        raise ValueError("Unknown evidence type")
    ref = data["reference_provenance"]
    judge = data["judge_provenance"]
    if (
        not isinstance(ref, dict)
        or set(ref) != {"type", "reviewer", "independent"}
        or ref["type"] not in ("human", "model", "synthetic")
        or type(ref["independent"]) is not bool
    ):
        raise ValueError("Invalid reference provenance")
    if ref["reviewer"] is not None and (
        not isinstance(ref["reviewer"], str) or not ref["reviewer"].strip()
    ):
        raise ValueError("Reviewer must be a nonempty identifier or null")
    if ref["type"] == "human" and ref["reviewer"] is None:
        raise ValueError("Human submissions require a credited identifier or pseudonym")
    if (
        not isinstance(judge, dict)
        or set(judge) != {"type", "model", "prompt_revision"}
        or judge["type"] not in ("model", "scripted")
    ):
        raise ValueError("Invalid judge provenance")
    if judge["type"] == "model" and not all(
        isinstance(judge[k], str) and judge[k].strip()
        for k in ("model", "prompt_revision")
    ):
        raise ValueError("Record the requested model and judge prompt revision")
    if data["evidence_type"] == "synthetic_fixture" and (
        ref["type"] != "synthetic" or judge["type"] != "scripted" or ref["independent"]
    ):
        raise ValueError(
            "Synthetic example must identify synthetic reference and scripted judge"
        )
    if not isinstance(data["rows"], list):
        raise ValueError("Rows must be a list")
    ids = set()
    groups = {}
    for row in data["rows"]:
        if not isinstance(row, dict) or set(row) != {
            "id",
            "group",
            "split",
            "reference",
            "judge",
        }:
            raise ValueError("Invalid row fields")
        if not all(isinstance(row[k], str) and row[k].strip() for k in row):
            raise ValueError("Row values must be nonempty strings")
        if row["id"] in ids:
            raise ValueError("Duplicate case ID")
        ids.add(row["id"])
        if (
            row["split"] not in ("calibration", "test")
            or row["reference"] not in ("pass", "fail", "uncertain", "unreviewed")
            or row["judge"] not in ("pass", "fail", "abstain", "missing")
        ):
            raise ValueError("Unknown split or verdict")
        if row["group"] in groups and groups[row["group"]] != row["split"]:
            raise ValueError("Related group crosses calibration/test boundary")
        groups[row["group"]] = row["split"]
    report = dict(
        evidence_status="synthetic demonstration only"
        if data["evidence_type"] == "synthetic_fixture"
        else "submitted comparison; provenance and independence self-reported, not verified",
        independent_review_verified=False,
        calibration_certified=False,
        reference_provenance=ref,
        judge_provenance=judge,
        splits={},
    )
    for split in ("calibration", "test"):
        rows = [r for r in data["rows"] if r["split"] == split]
        eligible = [r for r in rows if r["reference"] in ("pass", "fail")]
        matrix = {
            ref: {j: 0 for j in ("pass", "fail", "abstain", "missing")}
            for ref in ("pass", "fail")
        }
        for row in eligible:
            matrix[row["reference"]][row["judge"]] += 1
        decided = sum(matrix[r][j] for r in matrix for j in ("pass", "fail"))
        agreed = matrix["pass"]["pass"] + matrix["fail"]["fail"]
        report["splits"][split] = dict(
            total_rows=len(rows),
            matrix=matrix,
            reference_coverage=ratio(len(eligible), len(rows)),
            decision_coverage=ratio(decided, len(eligible)),
            agreement_on_decided=ratio(agreed, decided),
            false_acceptances=[
                r["id"]
                for r in eligible
                if r["reference"] == "fail" and r["judge"] == "pass"
            ],
            false_rejections=[
                r["id"]
                for r in eligible
                if r["reference"] == "pass" and r["judge"] == "fail"
            ],
            judge_abstentions=[r["id"] for r in eligible if r["judge"] == "abstain"],
            missing_judgments=[r["id"] for r in eligible if r["judge"] == "missing"],
            excluded_reference=[
                r["id"] for r in rows if r["reference"] not in ("pass", "fail")
            ],
        )
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compare(json.loads(args.packet.read_text()))
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as stream:
            stream.write(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
