"""Render the saved exploratory distribution; optional matplotlib dependency."""

import json
from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "results/analysis-2026-10-19/report.json").read_text())[
    "cluster_resampling"
]
fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
fig.patch.set_facecolor("#f4f1e9")
ax.set_facecolor("#f4f1e9")
counts = data["resampled_difference_counts"]
ax.hist(
    [x["difference"] for x in counts],
    weights=[x["count"] for x in counts],
    bins=[i / 20 for i in range(21)],
    color="#3e7863",
    edgecolor="#f4f1e9",
)
for bound in data["interval"]:
    ax.axvline(bound, color="#9b492c", linestyle="--", linewidth=1.5)
ax.axvline(
    data["observed_difference"],
    color="#183b35",
    linewidth=2,
    label="Observed difference: +0.50",
)
ax.set(
    xlim=(0, 1),
    xlabel="Difference in reference-span coverage (dense − BM25)",
    ylabel="Resample count",
    title="Conditional resampling of the authored retrieval set",
)
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.suptitle(
    "9 source-document clusters · 10,000 resamples · not a population confidence claim",
    fontsize=10,
    color="#555555",
)
fig.savefig(ROOT / "resampling.svg")
fig.savefig(ROOT / "resampling.png", dpi=150)
print("Rendered with matplotlib", matplotlib.__version__)
