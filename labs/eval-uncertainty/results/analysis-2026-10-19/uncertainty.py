"""Small inspectable statistical examples, not a substitute for study design."""

import math
import random
from collections import Counter, defaultdict
from statistics import NormalDist


def wilson(successes, total, confidence=0.95):
    if (
        type(successes) is not int
        or type(total) is not int
        or total <= 0
        or not 0 <= successes <= total
        or not 0 < confidence < 1
    ):
        raise ValueError(
            "Require integer 0 <= successes <= positive total and 0 < confidence < 1"
        )
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    p = successes / total
    denominator = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denominator
    radius = (
        z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    )
    return [max(0, center - radius), min(1, center + radius)]


def quantile(values, p):
    ordered = sorted(values)
    position = (len(ordered) - 1) * p
    low = math.floor(position)
    high = math.ceil(position)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def cluster_bootstrap(rows, resamples=10000, seed=42):
    if not rows or type(resamples) is not int or resamples <= 0:
        raise ValueError("Need observations and positive integer resamples")
    groups = defaultdict(list)
    for row in rows:
        groups[row["cluster"]].append(row["delta"])
    names = sorted(groups)
    rng = random.Random(seed)
    draws = []
    for _ in range(resamples):
        selected = [value for _ in names for value in groups[rng.choice(names)]]
        draws.append(sum(selected) / len(selected))
    return {
        "observations": len(rows),
        "clusters": len(names),
        "resamples": resamples,
        "seed": seed,
        "observed_difference": sum(row["delta"] for row in rows) / len(rows),
        "interval": [quantile(draws, 0.025), quantile(draws, 0.975)],
        "resampled_difference_counts": [
            {"difference": value, "count": count}
            for value, count in sorted(Counter(draws).items())
        ],
    }
