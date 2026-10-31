import numpy as np


def paired_bootstrap(a, b, n_boot=2000, seed=0, level=0.95):
    """Two models' per-item correctness on the same items: the mean difference a - b and a
    bootstrap interval that resamples items (keeping each pair). Return (diff, low, high)."""
    d = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    rng = np.random.default_rng(seed)
    means = d[rng.integers(0, len(d), (n_boot, len(d)))].mean(axis=1)
    lo, hi = np.quantile(means, [(1 - level) / 2, (1 + level) / 2])
    return float(d.mean()), float(lo), float(hi)
