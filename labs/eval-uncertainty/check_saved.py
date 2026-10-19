"""Recompute the exploratory report; no model calls or statistical-package dependencies."""

import hashlib, json
from pathlib import Path
from analyze import analysis

ROOT = Path(__file__).resolve().parent
out = ROOT / "results/analysis-2026-10-19"
saved = json.loads((out / "report.json").read_text())
for name, digest in saved["sha256"].items():
    assert hashlib.sha256((out / name).read_bytes()).hexdigest() == digest
assert {k: v for k, v in saved.items() if k != "sha256"} == analysis()
assert (
    sum(x["count"] for x in saved["cluster_resampling"]["resampled_difference_counts"])
    == 10000
)
assert saved["cluster_resampling"]["clusters"] == 9
print(
    "Verified all paired observations, 10,000 cluster resamples, source hash, and hypothetical Wilson intervals"
)
