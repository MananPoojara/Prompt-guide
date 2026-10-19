# 8. Follow a coding change from request to evidence

Previous: [Harnesses and loops](07-harnesses-and-loops.md) · Next: [Evaluation and failures](09-evaluation-and-failures.md)

A coding prompt is useful when it communicates the intended behavior and the boundaries of the change. The resulting code still needs inspection and execution. This repository includes a small saved change whose complete input, output, and tests fit on a few screens.

## Understand the behavior first

The function searches a list of product names. A user typing ` tea ` should be able to match a product named `Green Tea`: the extra spaces at the ends of the query should be ignored, and letter case should not prevent a match. The result should retain the products' original order and names.

The original [implementation](../labs/search-fix/before.py) did not normalize both sides of the comparison. The requested change is small enough that we can explain success before asking a model to implement it.

Here is the exact [recorded prompt](../labs/search-fix/prompt.txt):

```text
In search.py, make product search ignore leading/trailing query whitespace and match names without case sensitivity. Inspect the implementation and tests first. Preserve product ordering and empty-query behavior. Use no external dependencies. Do not change the tests. Implement the change, run the test suite, and report the change and actual result.
```

The first sentence defines the new behavior. “Inspect” tells the agent to gather local context. Preserving ordering and empty-query behavior protects existing behavior. “No external dependencies” prevents a small change from unnecessarily expanding the environment. “Do not change the tests” keeps the acceptance evidence stable for this demonstration.

That last constraint is appropriate to this fixture, not a universal rule that tests should never change. In ordinary development, a changed requirement may need changed tests. The point is to make the relationship between the requirement and the checks explicit.

## Read the resulting code

The saved [implementation](../labs/search-fix/after.py) is:

```python
def search_products(products, query):
    """Return matching product names in their original order."""
    query = query.strip().casefold()
    return [name for name in products if query in name.casefold()]
```

`strip()` removes whitespace at the ends of the query. `casefold()` produces a form intended for caseless comparison. The list comprehension examines products in their existing order and returns the original `name`, so normalization does not rewrite the displayed name.

The function still uses substring matching. It does not add typo correction, ranking, stemming, or semantic search. Those would be different requirements. Empty-query behavior remains tied to Python's substring semantics: the empty string is contained in every string, so all product names are returned.

## Inspect the checks instead of trusting the completion message

The [test file](../labs/search-fix/test_search.py) exercises five behaviors. The saved [before log](../labs/search-fix/before-tests.txt) shows three failures. The [after log](../labs/search-fix/after-tests.txt) shows all five passing. The raw [agent response](../labs/search-fix/response.txt) is preserved separately.

These artifacts support the statement: the recorded change made the five supplied checks pass, including the previously failing behaviors. They do not prove correctness for every possible Unicode string or every future caller. They also do not establish that this prompt is better than another prompt, because there was no comparison arm.

The [case README](../labs/search-fix/README.md) includes the runtime details and reproduction instructions. To verify the saved implementation, use a temporary directory so `search.py` resolves to the correct file:

```bash
trial_dir=$(mktemp -d)
cp labs/search-fix/after.py "$trial_dir/search.py"
cp labs/search-fix/test_search.py "$trial_dir/test_search.py"
(cd "$trial_dir" && python3 -m unittest -v)
```

No model is called by that command. It checks the saved generated code.

## What changes for a larger repository?

The same sequence expands: identify the affected behavior, inspect the relevant implementation and conventions, make a bounded change, run appropriate checks, and report limitations. Large projects introduce dependencies, migrations, services, concurrent changes, and deployment effects. A prompt that says “fix everything” leaves those decisions undefined.

A useful coding request states the observable outcome, the known scope, and any constraints that actually matter. The agent should discover the rest from the repository rather than inventing file names or APIs. The harness must expose the necessary tools and retain their results.

When a test fails, read the failure. It might indicate a regression, an unmet requirement, a missing dependency, or a test-environment problem. Those are different diagnoses. Changing a test solely to make the run green can erase the evidence that the requirement is still unmet.

Completion should connect the implementation to the observed checks: what changed, which behavior was verified, and which uncertainty remains. That habit is more transferable than any one coding prompt.
