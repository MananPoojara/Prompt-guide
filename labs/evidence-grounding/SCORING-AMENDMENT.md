# Scorer correction during recording

The model requests and documents were not changed. While recording was underway, additional unit tests exposed two scorer defects:

1. In the conflicting-current condition, both current documents state that registration is undecided. The initial scorer required a citation to current-plan specifically; either current source should be sufficient for that shared statement.
2. A non-string status could raise a TypeError instead of being counted as malformed output.

The live run retains its original frozen scorer and original manifest scores. The final report is recomputed with the corrected scorer and preserves both results for comparison. No model response is discarded or regenerated for this correction. Tests cover both defects. This aligns citation handling with the predeclared rule that a current supporting source is required; it does not change the input task or select favorable answers.
