# 2. Understand the failure before changing the words

A practical working model: the assistant generates a response conditioned on the instructions and information available in the current interaction. A fluent response is not a verification mechanism. A model can have useful learned knowledge and still lack your repository's current state, the newest documentation, or the product decision you have not stated.

## Five different problems that look like “bad prompting”

| Problem | Example | Useful intervention |
|---|---|---|
| Ambiguous objective | “Make it professional” | Give audience, constraints, and contrasting examples |
| Missing information | An invented API parameter | Retrieve the actual version's documentation |
| Conflicting context | Old and new requirements both appear | State which decision supersedes which |
| Execution failure | Correct plan, unavailable tool | Repair access or choose an available method |
| Weak verification | A claim that tests passed | Inspect command output and final artifacts |

Do not expect wording alone to repair missing permissions, incorrect data, or a tool that cannot reach its service.

## Context length is not the same as usable evidence

Liu and colleagues tested multi-document question answering and key-value retrieval and found sensitivity to the position of relevant information. This is evidence about the studied models and tasks, not a universal percentage penalty for modern models. [Lost in the Middle, 2023 revision](https://arxiv.org/abs/2307.03172)

Practical hypothesis to test: a small packet of relevant files plus clear references may outperform dumping every project document into the prompt. Evaluate this on your tasks; do not convert the paper into a magic ordering rule.

## Reasoning and self-correction

Ask for assumptions, a concise rationale, and evidence you can inspect. A long explanation can still be wrong. You do not need a private internal reasoning transcript to validate a calculation or a software change.

Huang and colleagues studied intrinsic self-correction without external feedback and found that it could fail or degrade reasoning performance. The paper does not prove that every current model or every feedback loop fails. [ICLR 2024 paper](https://arxiv.org/abs/2310.01798)

A better experiment supplies new evidence: a failing test, a counterexample, a source passage, or a human correction. Measure whether revision fixes the failure without breaking previously correct cases.

## Training, prompting, retrieval, and memory

These are different interventions. Prompting changes the input; retrieval brings selected external information into that input; persistent memory stores material that can be retrieved later. Fine-tuning changes model parameters through a training process. Saving a Markdown note does not itself train the model or guarantee that a future session will read it.


Next: [Context and memory](03-context-and-memory.md).
