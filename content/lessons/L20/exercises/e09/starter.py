import numpy as np


def pass_at_k(n, c, k):
    """Unbiased estimate of the chance that at least one of k samples is correct, from n samples
    of which c were correct: 1 - C(n - c, k) / C(n, k), computed as a product."""
    raise NotImplementedError


def mean_ci(scores, n_boot=2000, seed=0, level=0.95):
    """Mean of per-item scores with a percentile bootstrap interval over items.
    Return (mean, low, high)."""
    raise NotImplementedError
