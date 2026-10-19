# Compare judge decisions without hiding missing evidence

The [judge-comparison tool](../evaluation/judge-calibration/README.md) now reports calibration and test splits separately, including confusion tables, false-acceptance and false-rejection IDs, abstentions, missing judgments, and unreviewed or uncertain references. It rejects duplicate IDs and declared groups that cross the split boundary.

The worked example is **synthetic**: no human judgments or model-judge calls were made. Its test split illustrates 4/6 reference coverage, 3/4 decision coverage among usable references, and 1/3 agreement among decided cases. Its calibration split shows why perfect agreement can still hide missing judge outputs.

Eight tests and a deterministic example checker accompany the tool. The repository gate now checks 24 artifacts/check procedures, including this synthetic demonstration. Passing that gate does not establish judge calibration. The guide explains how to obtain references, freeze groups and thresholds, preserve failed judge calls, and keep a new test assessment separate from prompt development.

Independent human review and actual judge calibration remain open. Provenance is self-reported; the tool explicitly declines to certify independence or readiness.
