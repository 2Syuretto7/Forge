import numpy as np


def bootstrap_means(x, B, seed=0):
    """Return (B,) means of resamples of x drawn with replacement."""
    x = np.asarray(x, dtype=float)
    idx = np.random.default_rng(seed).integers(0, x.size, size=(B, x.size))
    return x[idx].mean(axis=1)


def percentile_ci(stats, level=0.95):
    """Equal-tailed percentile interval (lo, hi)."""
    lo, hi = np.quantile(stats, [(1 - level) / 2, (1 + level) / 2])
    return float(lo), float(hi)


def coverage(true_mean, datasets, B=500, level=0.95, seed=0):
    """Fraction of rows of datasets (R, n) whose bootstrap interval contains true_mean."""
    hits = 0
    for r, row in enumerate(np.asarray(datasets, dtype=float)):
        lo, hi = percentile_ci(bootstrap_means(row, B, seed + r), level)
        hits += lo <= true_mean <= hi
    return hits / len(datasets)
