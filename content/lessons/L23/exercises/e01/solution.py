import numpy as np


def accuracy_ci(correct, n_boot=2000, seed=0, level=0.95):
    """Accuracy over items (an array of 0/1) with a percentile bootstrap interval that resamples
    items. Return (accuracy, low, high)."""
    c = np.asarray(correct, dtype=float)
    rng = np.random.default_rng(seed)
    means = c[rng.integers(0, len(c), (n_boot, len(c)))].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, (1 + level) / 2])
    return float(c.mean()), float(lo), float(hi)


def standard_error(p, n):
    """The standard error of an accuracy p measured on n independent items."""
    return float(np.sqrt(p * (1 - p) / n))
