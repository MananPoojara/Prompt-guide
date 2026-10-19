# Representation recording protocol — 2026-10-19

Use the existing pinned DistilGPT2 revision and CPU environment from model-mechanics. Record two predeclared inputs: `The river bank is quiet.` and `The money bank is quiet.` The latter is deliberately simple wording for a financial context, not a naturalness benchmark. Require the token ` bank` to occur once at the same position in each input; fail rather than silently select another example.

Save token IDs, all token-embedding vectors, input hidden states (token plus position embeddings with dropout disabled), final hidden states after final layer norm, and attention weights for every head in every block. Keep both inputs and all heads, without selecting a heatmap to support a semantic claim. Compute cosine similarity for the bank token at the three stages. Do not interpret similarity as a calibrated measure of meaning or comprehension.

Model eval mode, no gradients, two CPU threads, deterministic algorithms. Save code/protocol hashes and versions. No generated answer or accuracy test is performed. Check causal masking, row sums, tensor dimensions, identical token/position inputs for the target, and measured change in contextual representation. The browser displays saved values, not live inference. A clean-environment reproduction is a separate verification step.
