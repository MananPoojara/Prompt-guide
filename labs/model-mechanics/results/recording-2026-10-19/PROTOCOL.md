# Model mechanics recording protocol

This lab illustrates actual tokenization and decoding on a pinned small text-completion model. It does not evaluate modern chat-model instruction following or prove that a prompt is good.

Use `distilbert/distilgpt2` revision `2290a62682d06624634c1f46a6ad5be0f47f38aa`, CPU, two threads, evaluation mode, and deterministic PyTorch operations. Record library versions and freeze the recorder, sampling function, and this protocol with SHA-256 hashes. Model weights are downloaded to the local cache, not redistributed in this repository.

Tokenize seven specified strings covering capitalization, leading whitespace, a long word, a non-English greeting, an emoji, and a date. Save IDs, individual decoded fragments, raw vocabulary pieces, and the full round-trip decode. Byte-level fragments may individually display a replacement character; the full ID sequence must decode to the original text.

Use two prefixes: “The capital of France is” and “The capital of Japan is”. Save the actual top 50 logits after each prefix. Run greedy continuation once, then top-50 sampling at temperatures 0.4, 1.0, and 1.6 with seeds 7, 23, and 41. Retain all 20 continuations across both prefixes, including repetition, factual mistakes, or incoherent text. Stop at end-of-text or 20 new tokens. No cherry-picking or prompt tuning after observing these outputs.

At every generation step, select the 50 highest model logits, divide by temperature, apply stable softmax over those 50, draw using a seeded Python random generator, and append the selected token. Save token IDs, selected ranks, and conditional probabilities. Recompute logits from the full accumulated sequence at every step. This deliberately simple implementation trades speed for inspectability and is not an optimized production serving loop.

Greedy decoding selects the highest-scoring token; it is represented by temperature 0 in the saved UI data, but does not call softmax with zero temperature. For sampled runs, higher temperature flattens the distribution over the same top-50 candidate set at a given step. It is not a factual-accuracy setting.

The browser recomputes temperature-adjusted probabilities from saved first-token logits. Its single-token draws are simulations from that saved distribution, not fresh model inference. The recorded continuation viewer shows complete saved runs; changing its selectors does not generate a new run. Arbitrary user text requires the Python recorder.

Seeded outputs are repeatable in the recorded environment; exact cross-platform or cross-version identity is not guaranteed. The model is an older English text-completion model, not a current instruction-tuned assistant. Tokenizer behavior on other scripts does not establish language understanding. No paid API, account, or user secrets are involved.
