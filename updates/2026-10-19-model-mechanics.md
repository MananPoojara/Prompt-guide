# 2026-10-19 — An inspectable model visual and everyday examples

[All updates](README.md)

## For readers who want to see what a model does

The new [model-mechanics lab](../labs/model-mechanics/README.md) shows actual token IDs, saved next-token scores, temperature-adjusted probabilities, and recorded continuations. Its browser visual works offline after downloading the repository. The Python recorder accepts your own short text and needs no paid model account.

The model is a pinned DistilGPT2 text-completion model, not a modern chat assistant. The browser uses retained data: moving the temperature slider recalculates probabilities over 50 candidates, while the continuation selectors display saved model runs. These are distinct operations and are labeled on the page.

All 20 default continuations are preserved, including repetition and incorrect claims. This demonstrates why fluent generation still needs verification; it does not establish an optimum temperature or a prompt-quality ranking.

## For readers who do not code

Three [everyday examples](../everyday/README.md) now include full input, exact request, actual output, and an explained check:

- Rewrite a workshop email while preserving logistical facts and uncertainty.
- Summarize library meeting notes while separating approvals from proposals.
- Explain a fraction misconception with checkable arithmetic.

One model response was recorded per example. The authoring assistant reviewed the facts and calculations. No independent human usability study or prompt comparison was performed.

## Verification and next work

A clean Python environment exactly reproduced the visual lab's retained tokenizations, scores, and continuations. Sampling tests, offline data checks, and desktop/mobile browser checks passed. Full package versions and model revision are recorded with the artifacts. Sources: the linked model card and generation reference in the lab.

The next development work is stronger evaluation data with explicit review status. The [roadmap](../ROADMAP.md) still distinguishes demonstrations from broader reliability evidence. No recurring monitoring job is introduced by this update.
