# Embeddings, context, and attention are different things

[Model chapter](../../handbook/02-model-and-context.md) · [Previous: tokens and sampling](../model-mechanics/README.md)

A token ID selects a row in a learned embedding table: a vector of numbers. In the recorded GPT-2 architecture, a positional vector is added before the transformer blocks. The blocks then update each position's representation using the allowed context. A token's initial lookup vector and its final contextual representation are therefore different objects.

**Open the visual:** download this directory and open `index.html` in your browser. It works offline with the included `data.js`, CSS, and JavaScript. GitHub's file preview does not execute it. Reading this page requires no installation. The visual performs no live inference.

## One token, two contexts

We recorded these two inputs with the same pinned DistilGPT2 model used in the sampling lab:

```text
The river bank is quiet.
The money bank is quiet.
```

The second sentence is deliberately simple financial-context wording. Both put the single token ` bank` at the same position. This controls the token lookup and its positional embedding while changing an earlier word. No output answer or word-sense accuracy test was performed.

| Bank representation | What was measured | Cosine similarity across inputs |
|---|---|---|
| Token embedding | Same vocabulary-table row | 1.000000 |
| Input hidden state | Token plus positional embedding, with dropout disabled | 1.000000 |
| Final hidden state | After all six blocks and final layer normalization | 0.990115 |

The first two vectors match coordinate for coordinate; the final vectors differ. They remain highly similar under cosine. This demonstrates context-dependent computation, **not** correct understanding of the two senses of “bank.” Cosine measures vector direction; its numerical value has no universal semantic threshold. The [raw recording](results/recording-2026-10-19/data.json) includes the full 768-dimensional vectors for every token, not only these summary values.

A retrieval embedding is another design choice: a model or pooling procedure produces a vector intended for comparing texts. This lab's token embeddings and final token states are not automatically a good sentence-search system. A retrieval method needs its own relevance evaluation.

## Read the attention matrix

The visual lets you choose either input, any of six blocks, and any of twelve heads. **All 144 matrices are retained.** Rows represent query positions; columns represent key positions. For this causal decoder, position 2 can use positions 0, 1, and 2, but not positions 3 onward. Each row's attention weights sum to approximately one in evaluation mode.

A simplified single-head operation is:

```text
scores = Q × transpose(K) / sqrt(head_dimension)
weights = softmax(scores + causal_mask)
mixed_values = weights × V
```

Here, Q, K, and V are learned projections of the incoming representations. Masked future positions receive zero weight after softmax. Each head has its own projections; the block also has an output projection, residual paths, normalization, and a feed-forward network. The matrix in the visual shows the weights, not the whole block's computation. The original Transformer paper develops the scaled dot-product mechanism; GPT-2's exact block arrangement is a separate implementation. [Primary paper](https://arxiv.org/abs/1706.03762) · [Pinned implementation](https://github.com/huggingface/transformers/blob/v4.33.3/src/transformers/models/gpt2/modeling_gpt2.py).

A bright cell does not prove that a word caused a correct answer. Attention alone can miss other computation paths and does not establish a causal explanation. Jain and Wallace's experiments provide one empirical reason to question that inference; their task-specific findings are not a measurement of this lab or every modern model. [Attention is not Explanation](https://aclanthology.org/N19-1357/).

## What this changes about prompting

Earlier supplied text can change later representations without changing trained parameters. That helps explain why adding relevant context can change an answer. It does not imply that adding more text always helps, that a particular word forces a particular computation, or that a persona prompt grants expertise. Check the actual task output and evidence separately.

The causal mask also explains why a token's representation in this recording cannot incorporate later tokens. An output generated after the complete prompt has a different available prefix. This observation is specific to the recorded causal architecture; it should not be generalized to all encoder or multimodal models.

## Reproduce and check

Recording needs Python and the [pinned dependencies](../model-mechanics/requirements.txt). A first run downloads model/tokenizer files; model weights are not included here. No paid API or login is required. Use a new output directory:

```bash
python3 -m venv /tmp/representation-env
/tmp/representation-env/bin/pip install -r labs/model-mechanics/requirements.txt
/tmp/representation-env/bin/python labs/representations/record.py --output /tmp/representation-recording
```

Add `--offline` once the exact model revision is cached. The committed run used the existing clean Python 3.10.12 environment with those pinned packages and CPU execution. A second execution in the separate system Python environment reproduced every saved vector and attention weight exactly. Versions, model revision, and source hashes are in the recording. The [protocol](PROTOCOL.md) fixed the two inputs before execution.

The standard-library checks validate dimensions, cosine calculations, source hashes, all causal masks and row sums, and the browser payload:

```bash
python3 -m unittest discover -s labs/representations -p 'test_*.py'
python3 labs/representations/check_saved.py
```

The [browser check](test_browser.cjs) uses Playwright/Chromium to exercise the controls, mobile width, and absence of external requests. It requires a separate Playwright installation. These checks validate the recording and interface; they do not prove semantic understanding or reveal proprietary model internals.
