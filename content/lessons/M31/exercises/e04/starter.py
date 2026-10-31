import math
import numpy as np


def union_epsilon(n, k, delta):
    """Half-width that holds for k estimates at once with probability 1 - delta."""
    raise NotImplementedError


def best_of_random(k, n, rng):
    """Best test accuracy among k random-guessing classifiers."""
    raise NotImplementedError


def expected_excess(k, n, trials, rng):
    """Average excess of the best accuracy over 1/2."""
    raise NotImplementedError
