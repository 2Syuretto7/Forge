import numpy as np


def mean_with_ci(values, n_boot=2000, seed=0, level=0.95):
    """The mean of per-example losses and a percentile bootstrap interval for it."""
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = values[rng.integers(0, len(values), (n_boot, len(values)))].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, (1 + level) / 2])
    return float(values.mean()), float(lo), float(hi)


def paired_difference(a, b, n_boot=2000, seed=0, level=0.95):
    """Two checkpoints scored on the same examples: the mean of a - b and a bootstrap interval that
    resamples examples (keeping each pair together)."""
    return mean_with_ci(np.asarray(a, dtype=float) - np.asarray(b, dtype=float), n_boot, seed, level)
