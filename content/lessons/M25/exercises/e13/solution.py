import numpy as np


def bootstrap_by_index(values, B, rng):
    """Bootstrap means by resampling indices."""
    v = np.asarray(values, dtype=float)
    return v[rng.integers(0, len(v), size=(B, len(v)))].mean(axis=1)


def bootstrap_by_counts(values, B, rng):
    """Bootstrap means from multinomial counts of the distinct values."""
    v = np.asarray(values, dtype=float)
    u, c = np.unique(v, return_counts=True)
    M = rng.multinomial(len(v), c / len(v), size=B)
    return M @ u / len(v)


def paired_interval(correct_a, correct_b, B, rng, level=0.95):
    """Percentile interval for the mean of correct_b - correct_a."""
    d = np.asarray(correct_b, dtype=float) - np.asarray(correct_a, dtype=float)
    m = bootstrap_by_counts(d, B, rng)
    lo, hi = np.quantile(m, [(1 - level) / 2, (1 + level) / 2])
    return float(lo), float(hi)
