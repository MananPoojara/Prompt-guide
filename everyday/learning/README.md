# Ask for an explanation you can check

[Everyday examples](../README.md) · [Prompt fundamentals](../../handbook/01-first-example.md)

The learner has a specific misconception: adding numerators and denominators separately. The request identifies that misconception and asks for a concrete representation, a calculation, and a reason the proposed answer is impossible.

This produces something the learner can examine, instead of merely being told that the answer is wrong.

## Supplied material

```text
Learner question:
"I think 1/2 + 1/3 = 2/5 because I added the top numbers and the bottom numbers. Why is that wrong?"
```

## Exact request

```text
Explain the learner's fraction mistake in plain language without shaming them. Use one concrete whole divided into equal-sized parts, show the correct calculation, and explain why 2/5 cannot be right by comparing it with 1/2. End with one similar question for the learner to try; place its answer in a separately labeled answer section. Keep the explanation under 250 words. Do not use tools.
```

## Recorded response

The following is the actual saved model output, with no content edits:

> It makes sense to try adding the top and bottom numbers. The tricky part is that the bottom number tells us the size of the pieces, so we need equal-sized pieces before we can add them.
>
> Imagine one chocolate bar divided into **6 equal pieces**:
>
> - **1/2** of the bar is **3 of those pieces**: 1/2 = 3/6.
> - **1/3** of the bar is **2 of those pieces**: 1/3 = 2/6.
>
> Together, that’s 5 pieces out of 6:
>
> **1/2 + 1/3 = 3/6 + 2/6 = 5/6.**
>
> The bottom number stays 6 because we’re still counting sixths. Adding pieces doesn’t change their size.
>
> Here’s another way to check: **2/5 is less than 1/2**, since 2/5 = 4/10 and 1/2 = 5/10. Adding a positive amount to 1/2 must give us more than 1/2, so 2/5 cannot be right.
>
> **Try it:** What is 1/2 + 1/4? Think of one whole divided into 4 equal parts.
>
> **Answer section**
>
> 1/2 + 1/4 = 2/4 + 1/4 = **3/4**.

[Raw response](response.txt) · [Complete assembled request](request.txt) · [Execution log](execution.log)

## Check the result

The recorded explanation divides one chocolate bar into six equal parts. It maps one half to three sixths and one third to two sixths, then adds them to get five sixths.

The independent arithmetic check is:

```text
1/2 + 1/3 = (3 + 2)/6 = 5/6
2/5 = 4/10 < 5/10 = 1/2
```

Adding a positive third to a half cannot yield a number smaller than that half. The response also supplies a similar question, `1/2 + 1/4`, and gives the correct answer `3/4` in a labeled answer section. It stays under 250 words.

These checks establish the arithmetic and requested structure, not that every learner will understand the analogy. No learner study was conducted.

## A failure to watch for

An explanation can reach the right numerical answer while using confusing language or an invalid analogy. Ask which part remains unclear, try a second representation, and check whether you can explain why the denominator must describe equal-sized parts.

The follow-up question is an optional way to check understanding, not a homework requirement for reading this resource.
