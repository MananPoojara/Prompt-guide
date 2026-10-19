# See text become tokens, then watch a model choose

[Learning roadmap](../../ROADMAP.md) · [Model explanation](../../handbook/02-model-and-context.md) · [Protocol](PROTOCOL.md)

This lab uses a real, downloadable text-completion model to make two mechanisms visible: how text becomes token IDs, and how generation settings change token selection. It keeps every recorded continuation, including repetition and incorrect claims.

**No paid model account is required.** The interactive page works offline with saved data. Generating new data requires installing Python dependencies and downloading model files once.

## Open the visual

Download or clone this repository, then open [index.html](index.html) in your browser. Keep `data.js`, `app.js`, and `style.css` beside it. GitHub's file viewer shows HTML source rather than running the visual.

Alternatively, from the repository root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8000/labs/model-mechanics/`. This serves your local checkout to your browser; it does not run inference or connect to an AI account.

The visual has three sections:

1. **Token boundaries:** select a recorded string and see the token IDs and decoded fragments.
2. **Next-token choices:** adjust temperature and inspect probabilities recalculated from actual saved logits. Draw one token from that distribution in the browser.
3. **Recorded continuations:** compare complete saved outputs across temperatures and random seeds. The seed dropdown selects recordings; it does not trigger a model call.

The text explanations, tables, and [full JSON artifact](results/recording-2026-10-19/data.json) provide alternatives to the charts. Controls are keyboard-accessible. Color is not the only way to distinguish tokens or probabilities.

## What is actually measured?

The tokenizer and model are `distilbert/distilgpt2`, pinned to revision `2290a62682d06624634c1f46a6ad5be0f47f38aa`. This is an older English text-completion model, not a modern instruction-following assistant. Its publisher's [model card](https://huggingface.co/distilbert/distilgpt2/tree/2290a62682d06624634c1f46a6ad5be0f47f38aa) describes its provenance and Apache-2.0 license. Model weights are cached outside the repository, not bundled here.

Seven strings were tokenized. For example, the actual IDs are:

| Input | Token IDs | Observation |
|---|---|---|
| `Hello world` | `15496, 995` | Two tokens for this tokenizer |
| ` Hello world` | `18435, 995` | A leading space changes the first token |
| `hello world` | `31373, 995` | Lowercase changes it again |
| `🧠` | `8582, 100, 254` | One displayed symbol spans three tokens |

These IDs belong to this vocabulary; they are not universal. A different tokenizer can split the same text differently. The non-English and emoji examples demonstrate representation, not language proficiency. Individual byte-derived fragments can show `�`; decoding the full ID sequence reconstructs the original string.

Two prefixes were used for generation: `The capital of France is` and `The capital of Japan is`. For each, we retained one greedy continuation and nine sampled continuations: temperatures 0.4, 1.0, and 1.6, each with seeds 7, 23, and 41. All 20 outputs are saved. The maximum continuation is 20 tokens, with earlier stopping on the model's end-of-text token.

## Read the probability chart correctly

A **logit** is a score before normalization. At each step, the recorder keeps the 50 highest scores. It then converts those scores into probabilities with:

```text
weight_i = exp((logit_i - largest_logit) / temperature)
probability_i = weight_i / sum(all 50 weights)
```

Subtracting the largest score is a numerical-stability measure. The displayed probability is **conditional on these 50 retained candidates**; discarded vocabulary tokens are excluded. The chart shows the top ten candidates and reports the remaining probability mass separately. Its bars use a fixed 0–100% scale.

Lower positive temperature concentrates probability on higher-scoring choices. Higher temperature flattens the distribution. Greedy decoding selects the highest-scoring token directly and does not use this formula at temperature zero. These are selection rules, not checks of truth. [Library generation reference](https://huggingface.co/docs/transformers/main/en/main_classes/text_generation).

At the next generation step, the selected token is part of the input. The model computes new scores for that new context. That is why a continuation is not merely repeated sampling from the first chart. The browser's draw button illustrates one selection from a fixed saved distribution; the Python recorder performs the actual multi-step process.

## The failures are part of the explanation

Some recorded continuations repeat themselves or make unsupported claims. The same low-temperature setting that concentrates choices can still produce a wrong statement. A random seed makes a sampling sequence repeatable under defined conditions; it does not make an answer true.

Do not read the geography-themed continuations as factual guidance. They are preserved model output, used to inspect decoding. This experiment does not establish an optimum temperature, compare modern assistants, measure prompt quality, or reveal a model's hidden reasoning.

## Check the saved data without the model

These commands use only Python's standard library:

```bash
python3 -m unittest discover -s labs/model-mechanics -p 'test_*.py'
python3 labs/model-mechanics/check_recording.py
```

The checker verifies frozen source hashes, record completeness, probability normalization, token-trace consistency, and that the browser data exactly matches the retained JSON. It does not rerun the model or prove factual correctness of its output.

## Generate new observations

The recording uses Python 3.10.12. To reproduce the pinned dependency environment with `uv` and CPU PyTorch:

```bash
uv venv --python 3.10 /tmp/prompt-guide-model-env
uv pip install --python /tmp/prompt-guide-model-env/bin/python \
  --torch-backend cpu -r labs/model-mechanics/requirements.txt
/tmp/prompt-guide-model-env/bin/python labs/model-mechanics/record.py \
  --output /tmp/my-model-recording
```

The first invocation downloads the model and tokenizer from Hugging Face. Model weights alone are roughly 330 MB, and Python dependencies need additional disk space. No GPU is required. The output directory must not exist: recordings are never silently overwritten.

Try your own text:

```bash
/tmp/prompt-guide-model-env/bin/python labs/model-mechanics/record.py \
  --tokenize-only --text "Your own short sentence."
/tmp/prompt-guide-model-env/bin/python labs/model-mechanics/record.py \
  --text "A helpful explanation begins with" --output /tmp/my-custom-recording
```

After the required files have been downloaded, add `--offline` to require the local cache. The custom-input path limits text to 500 characters. The requirements pin direct packages; transitive packages can vary. Exact output identity across platforms or library builds is not guaranteed.

`record.py` contains the full loop and uses the small standard-library [sampling implementation](sampling.py). The [recording directory](results/recording-2026-10-19) contains the frozen recorder, sampling code, protocol, and package metadata.

## Browser verification

The optional [browser test](test_browser.cjs) uses Playwright. To run it without adding packages to the repository:

```bash
npm install --prefix /tmp/prompt-guide-browser playwright@1.64.1
/tmp/prompt-guide-browser/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/prompt-guide-browser/node_modules node labs/model-mechanics/test_browser.cjs
```

It was executed successfully on desktop and 375-pixel mobile layouts; screenshots were visually inspected. It exercises token selection, temperature changes, sampling, recorded-output controls, and mobile overflow, and checks that the page makes no HTTP requests when opened as a local file.

The standard CI checks only the lightweight saved-data and Python tests. It does not download model weights or rerun inference on every push.

## Recorded verification

The retained data was generated on CPU with Python 3.10.12 and the package versions in its metadata. A separate clean `uv` environment reproduced all seven tokenizations, both first-token candidate sets, and all 20 continuations exactly. That is a local reproduction result, not a promise of bit-for-bit agreement on every platform.

Eight sampling tests passed. The saved-data checker passed. Playwright exercised the page at desktop and 375-pixel mobile widths without page errors or external network requests, and both screenshots were visually inspected. The model's incorrect and repetitive outputs were kept.
