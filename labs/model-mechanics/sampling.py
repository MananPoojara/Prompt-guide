"""Stable softmax and sampling over an already selected candidate set."""
import math

def probabilities(logits, temperature):
    if not logits or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError('Provide finite logits and a positive finite temperature')
    if not all(math.isfinite(x) for x in logits):
        raise ValueError('Logits must be finite')
    largest=max(logits)
    weights=[math.exp((x-largest)/temperature) for x in logits]
    total=sum(weights)
    return [x/total for x in weights]

def choose(probs, rng):
    if (not probs or any(not math.isfinite(p) or p<0 for p in probs)
            or not math.isclose(sum(probs),1,abs_tol=1e-9)):
        raise ValueError('Probabilities must be nonnegative, finite, and sum to one')
    point=rng.random()
    cumulative=0
    for index,p in enumerate(probs):
        cumulative+=p
        if point<cumulative: return index
    return max(i for i,p in enumerate(probs) if p>0)
