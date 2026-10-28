import numpy as np


def pass_at_k(n, c, k):
    """Unbiased estimate of the chance that at least one of k samples is correct, from n samples
    of which c were correct: 1 - C(n - c, k) / C(n, k), computed as a product."""
    if n - c < k:
        return 1.0
    return float(1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1)))


def mean_ci(scores, n_boot=2000, seed=0, level=0.95):
    """Mean of per-item scores with a percentile bootstrap interval over items.
    Return (mean, low, high)."""
    s = np.asarray(scores, dtype=float)
    rng = np.random.default_rng(seed)
    means = s[rng.integers(0, len(s), (n_boot, len(s)))].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, (1 + level) / 2])
    return float(s.mean()), float(lo), float(hi)
