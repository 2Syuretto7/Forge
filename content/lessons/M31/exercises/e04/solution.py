import math
import numpy as np


def union_epsilon(n, k, delta):
    """Half-width that holds for k estimates at once with probability 1 - delta."""
    return math.sqrt(math.log(2 * k / delta) / (2 * n))


def best_of_random(k, n, rng):
    """Best test accuracy among k random-guessing classifiers."""
    return float((rng.random((k, n)) < 0.5).mean(axis=1).max())


def expected_excess(k, n, trials, rng):
    """Average excess of the best accuracy over 1/2."""
    return float(np.mean([best_of_random(k, n, rng) - 0.5 for _ in range(trials)]))
