"""Verify the explicitly synthetic judge-comparison example; no human/model evidence."""

import json
from pathlib import Path
from compare import compare

root = Path(__file__).resolve().parent
packet = json.loads((root / "example.json").read_text())
assert packet["evidence_type"] == "synthetic_fixture"
report = compare(packet)
assert report == json.loads((root / "example-report.json").read_text())
assert report["evidence_status"] == "synthetic demonstration only"
assert not report["independent_review_verified"] and not report["calibration_certified"]
assert report["splits"]["test"]["reference_coverage"]["numerator"] == 4
assert report["splits"]["test"]["reference_coverage"]["denominator"] == 6
assert report["splits"]["test"]["agreement_on_decided"]["numerator"] == 1
assert report["splits"]["test"]["agreement_on_decided"]["denominator"] == 3
assert report["splits"]["calibration"]["missing_judgments"] == ["cal-missing"]
print(
    "Verified synthetic confusion table and coverage; no independent human review or actual model-judge calibration claimed."
)
