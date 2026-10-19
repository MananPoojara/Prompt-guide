# 2026-10-19 — Put the uncertainty assumptions beside the score

**For:** developers comparing prompts, retrievers, or agent workflows on small evaluations.

The [uncertainty lab](../labs/eval-uncertainty/README.md) reuses the saved retrieval outcomes to demonstrate paired resampling by source document. Ten questions form nine document groups. The observed dense-128 versus BM25-128 coverage difference is +0.50; the conditional 10,000-resample percentile range is +0.20 to +0.778.

That range is explicitly not presented as a justified population confidence claim: the documents and labels are authored, the comparison was selected after results, and independent review is pending. A separate hypothetical independent-trial example shows why 10/10 success is not certainty. A degenerate zero-difference example exposes another limitation of resampling.

**Evidence:** executable standard-library calculations, eight tests, exact report reconstruction, a pinned source-data hash, and a plotted distribution. No model calls or new labels were created. Statistical references are linked beside the corresponding explanations.

**Action:** report the sampling unit and dependencies before attaching an interval to a score. The evaluation guide, developer path, roadmap, and core audit now link the worked example; independent human review and judge calibration remain open.
